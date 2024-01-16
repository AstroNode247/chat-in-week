from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import model


template = """Let's work this out in a step by step way to be sure we have the right answer.
            Question: {question}. """
prompt = PromptTemplate(template=template, input_variables=["question"])

if __name__ == '__main__':
    print("Loading model...")
    # llm = model.get_model()
    llm_chain = model.conversation_chain()


    print("Press 'q' to quit")
    while True:
        question = input("User : ")
        if question == 'q':
            print("Bye")
            break
        else:
            answer = llm_chain.run(question)
            print(f'Answer : {answer}')

