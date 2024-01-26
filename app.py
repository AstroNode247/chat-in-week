import os
import streamlit as st
from chat import retrieval_chain, conversation_chain
from query import all_documents
from html_templates import css, bot_template, user_template
from rag import load_pdf_document, split_document, get_pdf_document

import tempfile

styl = f"""
<style>
    /* not great support for :has yet (hello FireFox), but using it for now */
    .element-container:has([aria-label="Select RAG mode"]) {{
      position: fixed;
      bottom: 0px;
      padding: 5px;
      z-index: 101;
    }}
    .stChatFloatingInputContainer {{
        bottom: 0px;
    }}

    /* Generate question text area */
    textarea[aria-label="Description"] {{
        height: 200px;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

st.header("MistRAG")

# >>>> UI interations <<<<

def handle_user_input(user_input):
    # TODO Add memory
    with st.spinner(""):
        response = st.session_state.conversation({'query': user_input})
    return response

def chat_input():
    user_input = st.chat_input("What service questions can I help you resolve today?")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            # Generate the response
            output = handle_user_input(user_input)['result']
            st.write(output)


            st.session_state[f"user_input"].append(user_input)
            st.session_state[f"generated"].append(output)


def display_chat():
    # Session state
    if "generated" not in st.session_state:
        st.session_state[f"generated"] = []

    if "user_input" not in st.session_state:
        st.session_state[f"user_input"] = []

    if "document" not in st.session_state:
        st.session_state.document = None

    if "rag_mode" not in st.session_state:
        st.session_state[f"rag_mode"] = []

    if st.session_state[f"generated"]:
        size = len(st.session_state[f"generated"])
        # Display only the last 10 exchanges
        for i in range(max(size - 10, 0), size):
            with st.chat_message("user"):
                st.write(st.session_state[f"user_input"][i])

            with st.chat_message("assistant"):
                st.write(st.session_state[f"generated"][i])

        with st.container():
            st.write("&nbsp;")
    if st.session_state.document:
        st.subheader(st.session_state.document)

def open_sidebar():
    st.session_state.open_sidebar = True


def close_sidebar():
    st.session_state.open_sidebar = False

def rename_chat(document):
    st.session_state.document = document

if not "open_sidebar" in st.session_state:
    st.session_state.open_sidebar = False
# if st.session_state.open_sidebar:
    # new_title, new_question = generate_ticket()
with st.sidebar:
    st.subheader("Choose a document")
    all_docs = all_documents()

    for doc in all_docs:
        if st.button(doc):
            with st.spinner("Processing"):
                st.session_state.conversation = retrieval_chain(doc)
                st.session_state[f"generated"] = []
                st.session_state[f"user_input"] = []
                rename_chat(doc)

    st.subheader("Or create a new one")
    collection_name = st.text_input("New document name")
    files = st.file_uploader(
        "Upload your PDFs here and click on 'Process'")
    if collection_name and files is not None:
        # create conversation chain
        if st.button("Process"):
            with st.spinner("Processing"):
                temp_dir = tempfile.mkdtemp()
                path = os.path.join(temp_dir, files.name)
                with open(path, "wb") as f:
                    f.write(files.getvalue())
                docs = load_pdf_document(path)
                docs = split_document(docs)
                st.session_state.conversation = retrieval_chain(collection_name, docs=docs)
                st.session_state[f"generated"] = []
                st.session_state[f"user_input"] = []

if __name__ == '__main__':
    # >>>> UI: show chat <<<<
    display_chat()
    chat_input()

