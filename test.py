# # # import streamlit as st
# # # import streamlit as stChat
# # # import google.generativeai as genai
# # # from dotenv import main
# # # import os
# # # from chat import chatter

# # # main.load_dotenv()
# # # API_KEY = os.getenv("GOOGLE_API_KEY")
# # # genai.configure(api_key=API_KEY)

# # # st.title("Welcome to Uber Assistance")

# # # # Initialize Gemini model
# # # model = genai.GenerativeModel("gemini-pro")

# # # # Initialize chat history
# # # if 'messages' not in st.session_state:
# # #   st.session_state.messages = []

# # # # Display chat messages from history
# # # for message in st.session_state.messages:
# # #   with st.chat_message(message["role"]):
# # #     st.markdown(message["text"])

# # # # React to user input
# # # prompt = st.chat_input("How may I help you?")
# # # if prompt:
# # #   with st.chat_message("user"):
# # #     st.markdown(prompt)
  
# # #   # Add user message to history
# # #   st.session_state.messages.append({"role": "user", "text": prompt})

# # #   # Chat with Gemini
# # #   response = model.start_chat(history=st.session_state.messages)
# # #   response = response.send_message(prompt, stream=True)

# # #   # Display streamed response
# # #   for chunk in response:
# # #     st.session_state.messages.append({"role": "assistant", "text": chunk.text})
# # #     with st.chat_message("assistant"):
# # #       st.markdown(chunk.text)

# # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # import streamlit as st
# # from streamlit_mic_recorder import mic_recorder, speech_to_text

# # state = st.session_state

# # if 'text_received' not in state:
# #     state.text_received = []

# # c1, c2 = st.columns(2)
# # with c1:
# #     st.write("Convert speech to text:")
# # with c2:
# #     text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

# # if text:
# #     state.text_received.append(text)

# # for text in state.text_received:
# #     st.text(text)

# # st.write("Record your voice, and play the recorded audio:")
# # audio = mic_recorder(start_prompt="⏺️", stop_prompt="⏹️", key='recorder')

# # if audio:
# #     st.audio(audio['bytes'])

# # # # # # # # # # # # # # # # # # # # #

# import streamlit as st
# from streamlit_mic_recorder import mic_recorder
# import io

# import speech_recognition as sr  # Import a speech-to-text library

# audio = mic_recorder(
#     start_prompt="Start recording",
#     stop_prompt="Stop recording",
#     just_once=False,
#     use_container_width=False,
#     format="webm",
#     callback=None,
#     args=(),
#     kwargs={},
#     key=None
# )

# if audio is not None:
#   audio_bytes = audio["bytes"]
#   with open("recorded_audio.webm", "wb") as f:
#       print(f.write(audio_bytes))

# # if audio:
# #     with sr.AudioFile(audio) as source:
# #         try:
# #             audio_text = sr.listen(source).recognize_google()  # Example using Google Speech-to-Text API
# #             st.write(audio_text)
# #         except sr.UnknownValueError:
# #             st.error("Could not understand audio")
# #         except sr.RequestError as e:
# #             st.error("Could not request results from speech recognition service; {0}".format(e))

# # with io.BytesIO(audio) as f:  # Create a file-like object from bytes
# #     with sr.AudioFile(f) as source:  # Pass the file-like object
# #         try:
# #             audio_text = r.listen(source).recognize_google()
# #             st.write(audio_text)
# #         except sr.UnknownValueError:
# #             st.error("Could not understand audio")
# #         except sr.RequestError as e:
# #             st.error("Could not request results from speech recognition service; {0}".format(e))

# import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
# from streamlit_bokeh_events import streamlit_bokeh_events

# stt_button = Button(label="Speak", width=100)

# stt_button.js_on_event("button_click", CustomJS(code="""
#     var recognition = new webkitSpeechRecognition();
#     recognition.continuous = true;
#     recognition.interimResults = true;
 
#     recognition.onresult = function (e) {
#         var value = "";
#         for (var i = e.resultIndex; i < e.results.length; ++i) {
#             if (e.results[i].isFinal) {
#                 value += e.results[i][0].transcript;
#             }
#         }
#         if ( value != "") {
#             document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
#         }
#     }
#     recognition.start();
#     """))

# result = streamlit_bokeh_events(
#     stt_button,
#     events="GET_TEXT",
#     key="listen",
#     refresh_on_update=False,
#     override_height=75,
#     debounce_time=0)

# if result:
#     if "GET_TEXT" in result:
#         st.write(result.get("GET_TEXT"))

# import streamlit as st
# import time

# st.set_page_config()

# ph = st.empty()
# N = 5*60
# for secs in range(N,0,-1):
#     mm, ss = secs//60, secs%60
#     ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
# #     time.sleep(1)

# import streamlit as st
# import time

# st.set_page_config(layout="wide")  # Ensure a wide layout for sidebar

# # --- Sidebar ---
# with st.sidebar:
#     ph = st.empty()
#     N = 5 * 60  # Set initial countdown duration (5 minutes)

#     # Run the countdown timer
#     for secs in range(N, 0, -1):
#         mm, ss = secs // 60, secs % 60
#         ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
#         time.sleep(1)

import asyncio        
import streamlit as st     
import time
from functools import partial
from datetime import datetime

def clock(field, name, starttime):
    """Print a time in a field"""
    tdelta =  datetime.now().replace(microsecond=0) - starttime.replace(microsecond=0)
    minutes, seconds = divmod(int(tdelta.total_seconds()), 60)      
    hours, minutes = divmod(minutes, 60)                                                                       
    field.metric(name, f"{hours}:{minutes:02d}:{seconds:02d}")

async def run_jobs(job_list):
    while True:
        for job in job_list:
            job()
        # Not sure why asyncio.sleep was used here...
        time.sleep(0.1)

col1, col2 = st.columns(2)
# Placeholder Fields for Timers
with col1:
    all_tasks = st.empty()
with col2:
    ph = st.empty()

jobs = []

# Jobs are queued for the fields
jobs.append(partial(clock, all_tasks, "foo", datetime(2023, 12, 28, 14)))
jobs.append(partial(clock, ph, "baz", datetime(2023, 12, 28, 16)))

if jobs:
    # not sure why asyncio is actually needed - a normal function works as well.
    asyncio.run(run_jobs(jobs))