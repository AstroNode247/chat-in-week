from langchain.prompts import PromptTemplate
from model import get_llm_model 
from rag import load_pdf_document, load_vectorized_docs, split_document

from langchain.chains import ConversationChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


def conversation_chain():
    template = """
    Respond to the human request. If you don't know the answer to a question, say I don't know.

    {history}
    Human: {input}
    AI Assistant:"""
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    conversation = ConversationChain(
        llm=get_llm_model(),
        prompt=PROMPT,
        verbose=True,
        memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
    )

    return conversation

def retrieval_chain(docs):
    db = load_vectorized_docs(docs)
    qa_chain = RetrievalQA.from_chain_type(
        get_llm_model(),
        retriever=db.as_retriever()
    )

    return qa_chain

if __name__ == '__main__':
    print("Loading model...")
    docs = load_pdf_document("pdfs\Selling_the_Invisible_A_Field_Guide_to_M.pdf")
    docs = split_document(docs)

    qa_chain = retrieval_chain(docs)


    print("Press 'q' to quit")
    while True:
        question = input("User : ")
        if question == 'q':
            print("Bye")
            break
        else:
            result = qa_chain({'query': question})
            answer = result['result']
            print(f'Answer : {answer}')

