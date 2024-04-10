import os
from abc import ABC

from dotenv import load_dotenv
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.llms import LlamaCpp
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()


class BaseLLM(ABC):
    def __init__(self):
        self.model = None
        self.embedding = None


class MistralLLM(BaseLLM):
    def __init__(self):
        super().__init__()
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        self.model = LlamaCpp(
            model_path="llm_model/mistral-7b-instruct-v0.2.Q5_K_M.gguf",
            temperature=0.5,
            n_ctx=1024,
            max_tokens=1000,
            top_p=1,
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
        )

        self.embedding = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-small-en",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )


class ChatGemini(BaseLLM):
    def __init__(self):
        super().__init__()
        API_KEY = os.getenv('GOOGLE_API_KEY')
        self.model = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.2, google_api_key=API_KEY,
                                            convert_system_message_to_human=True)
        self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)


