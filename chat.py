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
def role_to_streamlit(role: str) -> str:
    if role == 'model':
        return 'assistant'
    else:
        return role

def chatter(mod, prompty):
    finishDebate = st.button("End Debate", key=2)
    try:
        if "chat" not in st.session_state:
            st.session_state.chat = mod.start_chat(history=[])

        for message in st.session_state.chat.history:
            with st.chat_message(role_to_streamlit(message.role)):
                st.markdown(message.parts[0].text)
        if prompt := st.chat_input("Debate me!"):
            st.chat_message("user").markdown(prompt)
            response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f'An error occurred: {e}')
    # # Initialize chat history
    # if 'messages' not in st.session_state:
    #     st.session_state.messages = [prompty]

    # # Display chat messages from history
    # for message in st.session_state.messages[1:]:
    #     print (message)
    #     with st.chat_message(message['role']):
    #         st.markdown(message['content'])

    # # React to user input
    # prompt = st.chat_input("Write your argument here!")
    # if prompt:
    #     with st.chat_message("user"):
    #         st.markdown(prompt)

    #     st.session_state.messages.append(prompt)

    #     # messages_list = [
    #     #         {"role": m["role"], "content": m["content"]} 
    #     #         for m in st.session_state.messages
    #     # ]
        
    #     with st.chat_message("assistant"):
    #         message_placeholder = st.empty()
    #         full_response = ""
    #         model = mod
    #         chat = model.start_chat(history=[])
    #         response = chat.send_message(prompty + prompt)
    #         message_placeholder.markdown(response.text + " ")
    #         st.session_state.messages.append(response.text)
    #         i = 0

    #         while not (finishDebate):
    #             if response:
    #                 response = chat.send_message(prompt)
    #                 message_placeholder.markdown(response.text + " ")
    #                 st.session_state.messages.append(response.text)
            # if (finishDebate):
            #     return



            # for response in client.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=messages_list,
            #     stream=True,
            # ):
                # content = response.choices[0].delta.content if hasattr(response.choices[0].delta, 'content') else None
                # if content is not None:
                #     full_response += content




