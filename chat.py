from abc import ABC, abstractmethod

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from langchain_core.runnables.history import RunnableWithMessageHistory

from model import BaseLLM, ChatGemini
from rag import FileLoader, PDFLoader


class PromptTemplateManagement(ABC):
    """Conversation management from history, prompt template to RAG prompt.
    Wrapper for the underlying chat state between the user and the chatbot.
    It is used as context for handling the behavior of the chatbot by leveraging the system prompt."""

    def __init__(self, ):
        self.chat_template = None

    @abstractmethod
    def make_chat_prompt(self, system_prompt):
        """Create ChatTemplate based prompt to integrate a system prompt and a human messages"""
        pass


class PromptTemplate(PromptTemplateManagement):
    def __init__(self):
        super().__init__()

    def make_chat_prompt(self, system_prompt):
        self.chat_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])
        return self.chat_template


class Chat(ABC):
    def __init__(self, llm: BaseLLM, system_prompt: str):
        self.llm = llm
        self.chat_template = None
        self.chat_history = None
        self._chain = None

    def get_chain(self):
        return self._chain

    def chat(self, message: str):
        ai_response = self._chain.invoke(
            {"input": message},
            {"configurable": {"session_id": "unused"}}
        )
        return ai_response
    
    
    def add_history(self, type: str = None):
        if not type:
            return self._chain
        elif type == "summarize":
            self._chain = (
                    RunnablePassthrough.assign(messages_summarized=self._summarize_messages)
                    | self._chain
            )
        elif type == "trim":
            self._chain = (
                    RunnablePassthrough.assign(messages_summarized=self._trim_messages)
                    | self._chain
            )
        elif type == "hybrid":
            self._chain = (
                    RunnablePassthrough.assign(messages_summarized=self._trim_and_summarize_messages)
                    | self._chain
            )
        else:
            raise TypeError(f"Type should be 'summarize' or 'trim' or 'None'")
        return self._chain


    def _summarize_messages(self, chain_input):
        stored_messages = self.chat_history.messages
        if len(stored_messages) == 0:
            return False

        prompt = "Distill the above chat messages into a single summary message.\
                 Include as many specific details as you can."
        summarization_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "user",
                prompt
            ),
        ])
        summarization_chain = summarization_prompt | self.llm.model
        summary_message = summarization_chain.invoke({"chat_history": stored_messages})
        self.chat_history.clear()
        self.chat_history.add_user_message(prompt)
        self.chat_history.add_ai_message(summary_message.content)
        return True

    def _trim_messages(self, chain_input):
        stored_messages = self.chat_history.messages
        if len(stored_messages) <= 2:
            return False

        self.chat_history.clear()

        for message in stored_messages[-2:]:
            self.chat_history.add_message(message)

        return True

    def _trim_and_summarize_messages(self, chain_input):
        n_messages = 4
        stored_messages = self.chat_history.messages
        self.chat_history.clear()
        if len(stored_messages) == 0:
            return False

        if len(stored_messages) > n_messages:
            prompt = "Distill the above chat messages into a single summary message.\
             Include as many specific details as you can."
            summarization_prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "user",
                    prompt
                ),
            ])

            summarization_chain = summarization_prompt | self.llm.model
            summary_message = summarization_chain.invoke({"chat_history": stored_messages[:-n_messages]})

            self.chat_history.add_user_message(prompt)
            self.chat_history.add_ai_message(summary_message.content)

        for message in stored_messages[-n_messages:]:
            self.chat_history.add_message(message)


class ChatWithData(Chat):
    """Build the all stuff for generating the chatbot for RAG case. Chain them together and load the chatbot
    to chat with human."""

    def __init__(self, llm: BaseLLM, system_prompt: str = """
    Answer the user's questions based on the below context.
    
    <context>
    {context}
    </context>
    """):
        super().__init__(llm, system_prompt)
        self.db = None
        self.llm = llm
        self.chat_template = PromptTemplate().make_chat_prompt(system_prompt)
        self.query_template = PromptTemplate().make_chat_prompt(
            """Answer the user's questions based on the below context.""")
        self.chat_history = ChatMessageHistory()
        self._chain = None
        self._query_chain = None

    def make_chain(self, collection_name: str, loader: FileLoader = None, path: str = None):
        self.db = loader.load_embeddings(path=path, collection_name=collection_name, llm=self.llm)
        retriever = self.db.as_retriever()

        self._query_chain = self.query_template | self.llm.model
        self._query_chain = RunnableWithMessageHistory(
            self._query_chain,
            lambda session_id: self.chat_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )

        self._query_chain = RunnableBranch(
            (
                lambda x: len(x.get("chat_history", [])) == 1,
                (lambda x: x["chat_history"][-1].content) | retriever
            ),
            self._query_chain | StrOutputParser() | retriever
        ).with_config(run_name="chat_mode")

        document_chain = self.chat_template | self.llm.model
        document_chain = RunnableWithMessageHistory(
            document_chain,
            lambda session_id: self.chat_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )
        self._chain = RunnablePassthrough.assign(
            context=self._query_chain
        ).assign(answer=document_chain)



class ChatBot(Chat):

    def __init__(self, llm: BaseLLM, system_prompt: str):
        super().__init__(llm, system_prompt)
        self.llm = llm
        self.chat_template = PromptTemplate().make_chat_prompt(system_prompt)
        self.chat_history = ChatMessageHistory()
        self._chain = self.chat_template | self.llm.model
        self._chain = RunnableWithMessageHistory(
            self._chain,
            lambda session_id: self.chat_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )


if __name__ == '__main__':
    print("Loading model...")
    chatbot = ChatWithData(ChatGemini())
    chatbot.make_chain("Selling_Invisible", PDFLoader())
    chatbot.add_history("trim")
    
    print("Press 'q' to quit")
    while True:
        question = input("User : ")
        if question == 'q':
            print("Bye")
            print(chatbot.chat_history.messages)
            break
        else:
            answer = chatbot.chat(question)
            print(f'Answer : \n{answer["answer"].content}')
