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

def retrieval_chain(collection_name, docs=None):
    template = """Use the following context to answer the question at the end.
    If you don't know the answer, just say you don't know, don't try to make up an answer.
    Always say “Thanks for asking!” » at the end of the answer.

    {context}

    Question: {question}

    Helpful answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    db = load_vectorized_docs(collection_name, docs=docs)
    qa_chain = RetrievalQA.from_chain_type(
        get_llm_model(),
        retriever=db.as_retriever(),
        verbose=True,
        chain_type_kwargs={'prompt': QA_CHAIN_PROMPT}
    )

    return qa_chain


def recommendation_chain(collection_name, docs=None):
    template = """You are a sales person that sale users electronic product that match their preferences. 
    For each question, suggest three product, with a short description of the plot and the reason why the user migth like it.
    If the user request is not clear, ask for more information.
    Use only the following pieces of data to recommand to the user at the end. When you have finished 
    to recommend ask this question : "What else can I do ?"  

    {context}

    user: {question}
    Your response:"""

    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    db = load_vectorized_docs(collection_name, docs=docs)
    qa_chain = RetrievalQA.from_chain_type(
        get_llm_model(),
        retriever=db.as_retriever(),
        verbose=True,
        chain_type_kwargs={'prompt': QA_CHAIN_PROMPT}
    )

    return qa_chain

if __name__ == '__main__':
    print("Loading model...")
    # docs = load_pdf_document("pdfs\Selling_the_Invisible_A_Field_Guide_to_M.pdf")
    # docs = split_document(docs)

    qa_chain = retrieval_chain(collection_name="Event_Ecom", 
                               docs=None)


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

