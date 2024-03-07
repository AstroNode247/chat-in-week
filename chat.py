from abc import ABC, abstractmethod

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from model import BaseLLM, ChatGemini
from rag import PDFLoader, FileLoader


class Chat:
    """Build the all stuff for generating the chatbot for RAG case. Chain them together and load the chatbot
    to chat with human."""

    def __init__(self):
        self.db = None
        self.llm = None

    def chain(self, llm: BaseLLM, loader: FileLoader, collection_name: str, path: str = None):
        self.llm = llm
        self.db = loader.load_embeddings(llm=self.llm,
                                         collection_name=collection_name,
                                         path=path)

        system_prompt = """Use the following context to answer the question at the end. Detail the answer
                to provide the most insightful response.
            
                {context}"""

        chat_template = RAGConversation().make_chat_prompt(system_prompt)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
                {"context": self.db.as_retriever() | format_docs, "question": RunnablePassthrough()}
                | chat_template
                | self.llm.model
                | StrOutputParser()
        )
        return rag_chain


class ConversationManagement(ABC):
    """Conversation management from history, prompt template to RAG prompt.
    Wrapper for the underlying chat state between the user and the chatbot.
    It is used as context for handling the behavior of the chatbot by leveraging the system prompt."""

    def __init__(self,):
        self.chat_template = None

    @abstractmethod
    def make_chat_prompt(self, system_prompt):
        """Create ChatTemplate based prompt to integrate a system prompt and a human messages"""
        pass


class RAGConversation(ConversationManagement):
    """Manage a RAG based Chatbot. A RAG prompt must contains a {context} and a {question} keyword"""
    def __init__(self):
        super().__init__()

    def make_chat_prompt(self, system_prompt):
        """Create a chat template that best suit the RAG management system"""
        self.chat_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}")
        ])
        return self.chat_template


# def conversation_chain():
#     template = """
#     Respond to the human request. If you don't know the answer to a question, say I don't know.
#
#     {history}
#     Human: {input}
#     AI Assistant:"""
#     PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
#     conversation = ConversationChain(
#         llm=get_llm_model(),
#         prompt=PROMPT,
#         verbose=True,
#         memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
#     )
#
#     qa_chain = RetrievalQA.from_chain_type(
#         get_llm_model(),
#         retriever=db.as_retriever(),
#         verbose=True,
#         chain_type_kwargs={'prompt': QA_CHAIN_PROMPT}
#     )
#     return conversation
#
#
# def retrieval_chain(collection_name, docs=None):
#     template = """Use the following context to answer the question at the end.
#     If you don't know the answer, just say you don't know, don't try to make up an answer.
#     Always say “Thanks for asking!” » at the end of the answer.
#
#     {context}
#
#     Question: {question}
#
#     Helpful answer:"""
#     QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
#
#     db = load_vectorized_docs(collection_name, docs=docs)
#     return qa_chain
#
#
# def recommendation_chain(collection_name, docs=None):
#     template = """You are a sales person that sale users electronic product that match their preferences.
#     For each question, suggest three product, with a short description of the plot and the reason why the user migth like it.
#     If the user request is not clear, ask for more information.
#     Use only the following pieces of data to recommand to the user at the end. When you have finished
#     to recommend ask this question : "What else can I do ?"
#
#     {context}
#
#     user: {question}
#     Your response:"""
#
#     QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
#
#     db = load_vectorized_docs(collection_name, docs=docs)
#     qa_chain = RetrievalQA.from_chain_type(
#         get_llm_model(),
#         retriever=db.as_retriever(),
#         verbose=True,
#         chain_type_kwargs={'prompt': QA_CHAIN_PROMPT}
#     )
#
#     return qa_chain


if __name__ == '__main__':
    print("Loading model...")
    qa_chain = Chat().chain(ChatGemini(), PDFLoader(), collection_name="Invisible_Man")

    print("Press 'q' to quit")
    while True:
        question = input("User : ")
        if question == 'q':
            print("Bye")
            break
        else:
            result = qa_chain.invoke(question)
            answer = result
            print(f'Answer : \n{answer}')
