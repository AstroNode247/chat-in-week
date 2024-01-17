from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


def get_model():
    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        model_path="llm_model\mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )
    return llm

def conversation_chain():
    template = """
    Respond to the human request. If you don't know the answer to a question, say I don't know.

    {history}
    Human: {input}
    AI Assistant:"""
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    conversation = ConversationChain(
        llm=get_model(),
        prompt=PROMPT,
        verbose=True,
        memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
    )

    return conversation