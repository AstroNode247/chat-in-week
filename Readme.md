# Chatbot for Local Machine

You can chat with this chatbot without an internet connection. All you need to do is upload your document to the app and ask your questions about it. You don't necessarily need a powerful PC to run the model on your local machine. For optimal performance, it is recommended to have at least 16GB of RAM and a Core i5 5th generation processor. The chatbot will also run on 12GB RAM, but it may be slower.

## Requirements:

* Python 3.11
* Download **openhermes-0.2.5-mistral-7b** or **mistral-7b-instruct** GGUF version, which you can download on Hugging Face. 
* Create a folder named llm_model and place the model there.
* Create your Python environment and run `pip install requirements.txt` to install all necessary packages.
* Install Milvus with Docker.

Finally, enjoy the chatbot experience with `streamlit run app.py.`"