from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import model


if __name__ == '__main__':
    print("Loading model...")
    conversation = model.conversation_chain()


    print("Press 'q' to quit")
    while True:
        question = input("User : ")
        if question == 'q':
            print("Bye")
            break
        else:
            answer = conversation.predict(input=question)
            print(f'Answer : {answer}')

