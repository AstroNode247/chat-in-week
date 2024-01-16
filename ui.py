import streamlit as st
from html_templates import css, bot_template, user_template

def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    st.write(user_template.replace(
                "{{MSG}}", "Hello world"), unsafe_allow_html=True)
    st.write(bot_template.replace(
                "{{MSG}}", "Hello you"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        

if __name__ == "__main__":
    main()