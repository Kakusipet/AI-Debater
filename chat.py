import streamlit as st
# from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# client = OpenAI(
#   api_key=os.environ['OPENAI_API_KEY'], 
# )

# if model not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"


def chatter(mod, prompty):
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [prompty]

    # Display chat messages from history
    for message in st.session_state.messages[1:]:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # React to user input
    prompt = st.chat_input("How may I help you")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append(prompt)

        # messages_list = [
        #         {"role": m["role"], "content": m["content"]} 
        #         for m in st.session_state.messages
        # ]

        with st.chat_message("assistant"):
            message_placeholer = st.empty()
            full_response = ""
            model = mod
            chat = model.start_chat(history=[])
            response = chat.send_message(prompty)
            
            # for response in client.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=messages_list,
            #     stream=True,
            # ):
                # content = response.choices[0].delta.content if hasattr(response.choices[0].delta, 'content') else None
                # if content is not None:
                #     full_response += content

                message_placeholer.markdown(full_response + " ")
        st.session_state.messages.append(full_response)


