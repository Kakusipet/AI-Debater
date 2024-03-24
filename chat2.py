import os
import streamlit as st
import google.generativeai as genai

def role_to_streamlit(role: str) -> str:
    if role == 'model':
        return 'assistant'
    else:
        return role

def log_to_string():
    chat_history = st.session_state.chat.history
    log_string = ""
    for message in chat_history[2:]:
        role = role_to_streamlit(message.role)
        text = message.parts[0].text
        log_string += f"{role}: {text}\n"
    return log_string

def chatter(mod, prompty, side):
    try:
        model = mod

        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            st.session_state.chat.send_message(prompty)
            #st.session_state.chat.history.append({"role":"system", "parts" : {"text" : prompty}})
        # st.title('Gemini Pro Test')
        # print(st.session_state.chat.history)
        if (side == "Pro"):
            for message in st.session_state.chat.history[2:]:
                with st.chat_message(role_to_streamlit(message.role)):
                    st.markdown(message.parts[0].text)
        if (side == "Con"):
            for message in st.session_state.chat.history[1:]:
                with st.chat_message(role_to_streamlit(message.role)):
                    st.markdown(message.parts[0].text)

        if prompt := st.chat_input("Argue!"):
            st.chat_message("user").markdown(prompt)
            response = st.session_state.chat.send_message(prompt, safety_settings=[
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
])
            with st.chat_message("assistant"):
                st.markdown(response.text)
    except Exception as e:
        st.error(f'An error occurred: {e}')