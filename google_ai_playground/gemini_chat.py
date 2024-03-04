from getpass import getpass 
import textwrap

from langchain_google_genai import GoogleGenerativeAI
import google.generativeai as genai

from IPython import display
from IPython.display import Markdown


GOOGLE_API_KEY = 'AIzaSyAgSarNBFh183G4pISFmfc_C7Smc6x6la0'

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("What is the meaning of life?")
print(response.text)
