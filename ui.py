import os
import streamlit as st
from chat import retrieval_chain, conversation_chain
from html_templates import css, bot_template, user_template
from rag import load_pdf_document, split_document, get_pdf_document

import tempfile


def handle_user_input(user_input):
    # TODO Add memory
    response = st.session_state.conversation({'query': user_input})
    st.session_state.chat_history.extend([response['query'], response['result']])
    for i, message in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.write(user_template.replace(
                        "{{MSG}}", message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                        "{{MSG}}", message), unsafe_allow_html=True)


@st.cache_resource
def initiate_model():
#     # This function will only be run the first time it's called
#     st.session_state.conversation = model.conversation_chain()
    st.session_state.chat_history = []

def main():
    st.set_page_config(page_title="MistRAG",
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

    with st.sidebar:
        st.subheader("Your documents")
        files = st.file_uploader(
            "Upload your PDFs here and click on 'Process'")
        if st.button("Process"):
            with st.spinner("Processing"):
                if files is not None:
                    temp_dir = tempfile.mkdtemp()
                    path = os.path.join(temp_dir, files.name)
                    with open(path, "wb") as f:
                        f.write(files.getvalue())
                    docs = load_pdf_document(path)
                    docs = split_document(docs)

                    # create conversation chain
                    st.session_state.conversation = retrieval_chain(docs)
                else:
                    st.write("No file uploaded")


if __name__ == "__main__":
    main()