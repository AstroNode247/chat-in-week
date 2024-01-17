import streamlit as st
import model 
from html_templates import css, bot_template, user_template


def handle_user_input(user_input):
    response = st.session_state.conversation.predict(input=user_input)
    st.session_state.chat_history.extend([user_input, response])
    for i, message in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.write(user_template.replace(
                        "{{MSG}}", message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                        "{{MSG}}", message), unsafe_allow_html=True)


@st.cache_resource
def initiate_model():
    # This function will only be run the first time it's called
    st.session_state.conversation = model.conversation_chain()
    st.session_state.chat_history = []

def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    initiate_model()

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question)
        

if __name__ == "__main__":
    main()