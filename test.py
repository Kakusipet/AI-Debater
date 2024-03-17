import streamlit as st
import streamlit as stChat
import google.generativeai as genai
from dotenv import main
import os
from chat import chatter

main.load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

st.title("Welcome to Uber Assistance")

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Initialize chat history
if 'messages' not in st.session_state:
  st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["text"])

# React to user input
prompt = st.chat_input("How may I help you?")
if prompt:
  with st.chat_message("user"):
    st.markdown(prompt)
  
  # Add user message to history
  st.session_state.messages.append({"role": "user", "text": prompt})

  # Chat with Gemini
  response = model.start_chat(history=st.session_state.messages)
  response = response.send_message(prompt, stream=True)

  # Display streamed response
  for chunk in response:
    st.session_state.messages.append({"role": "assistant", "text": chunk.text})
    with st.chat_message("assistant"):
      st.markdown(chunk.text)
