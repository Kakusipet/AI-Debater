import streamlit as st
import streamlit as stChat
import google.generativeai as genai
from dotenv import main
import os
from chat2 import chatter, log_to_string
import random as rand
import time

# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma, FAISS
# from langchain.chains.question_answering import load_qa_chain

main.load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

#st.title("AI Debater")
#st.title('_Streamlit_ is :blue[cool] :sunglasses:')

def nextPg(): 
    st.session_state.page += 1
    st.rerun()

def prevPg(): 
    st.session_state.page -= 1
    st.rerun()

def genTopic():
    return model.generate_content("Generate only ONE debate topic. Do NOT generate more than one debate topic. Only return the topic with NO other numbers or text. Do not give any topics against google's terms. Make sure the topic is interesting and unique. The topic could relate to social and political issues, education, health, technology, environment or more. Return in the format 'Resolved:' ")

def genFeedback():
    str = log_to_string()
    st.write(model.generate_content(f"Act as the judge of a debate competition. The topic is {st.session_state.debateTopic} and you are advising the {st.session_state.debateSide} speaker, user. Provide feedback on user's performance against user's opponent: AI. The feedback should be based on delivery, content, style, and overall responses to opponent AI's arguments. At the end, declare the winner of the competition between user and AI keeping in mind that user's skill level is only {st.session_state.skillStr}. Be very honest and critical." + str, safety_settings=[
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
]).text)

def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.audio(audio_bytes)

if "page" not in st.session_state:
    st.session_state.page = 0

pg = st.empty()

# # # # # # # # PROMPT VARIABLES # # # # # # # #

skillLvl = 0
debateForm = ''
debateSide = ''
debateTopic = ''
rTime = 0
dTime = 0

chatLog = ""

# # # # # # # # PROMPT VARIABLES # # # # # # # #



if st.session_state.page == 0:
    # Replace the placeholder with some text:

    st.markdown("<h1 style='text-align: center; color: white;'>AI Debater</h1>", unsafe_allow_html=True)
    # st.markdown("<img src=\"ai_debate_logo.png\" alt=\"Italian Trulli\">", unsafe_allow_html=True)
    col1, col2, col3 = pg.columns(3)
    startButton = col2.button("Begin Your Debating Journey")
    col2.image("ai_debate_logo.png")

    if (startButton):
        nextPg()

elif st.session_state.page == 1:
        
    st.markdown("<h1 style='text-align: center; color: white;'>How experienced are you with debate?</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    newButt = col1.button("Beginner")
    midButt = col2.button("Intermediate")
    expButt = col3.button("Experienced")
    if (newButt):
        st.session_state.skillLvl = 1
        st.session_state.skillStr = "beginner"
        nextPg()
    elif (midButt):
        st.session_state.skillLvl = 2
        st.session_state.skillStr = "intermediate"
        nextPg()
    elif (expButt):
        st.session_state.skillLvl = 3
        st.session_state.skillStr = "experienced"
        nextPg()

elif st.session_state.page == 2:
    col1, col2, col3 = pg.columns(3)
    debateFormButt = col2.button("Submit")
    option = col2.selectbox(
    'What debate format would you like?',
    ('', 'Standard'))
    if (option == 'Standard'):
        col2.write("This is normal debating")
        desc = "In a regular debate, you have time to debate and take turns arguing points."
    # elif (option == 'Crossfire'):
    #     col2.write("This is fiery debating")
    #     desc = ""
    # elif (option == 'Thought Talk'):
    #     col2.write("This is relaxed debating")
    #     desc = "In a thought talk, you can express any thoughts on the topic without picking any side"
    # if (option == '')
    if (debateFormButt):
        if (option == ''):
            col2.write("Pick one of the options")
        else: 
            st.session_state.debateForm = option
            st.session_state.debateFormDesc = option + desc

            nextPg()

elif st.session_state.page == 3:
    st.markdown("<h1 style='text-align: center; color: white;'>Topic</h1>", unsafe_allow_html=True)

    # Generate the topic only once, initially
    if "topic1" not in st.session_state:
        st.session_state.topic1 = ""

    randButt = st.button("Randomize")
    if (randButt):
        st.session_state.topic1 = genTopic().text

    topicIn = st.text_input("Enter a topic of your choice", value=st.session_state.topic1)


    
    if (st.session_state.debateForm != 'Thought Talk'):
        side = st.radio(
        "What side will you argue",
        ["Pro", "Con", "Either"])
        if (side == "Either"):
            if (rand.randint(0, 1) == 0):
                side = "Pro"
            else:
                side = "Con"
                    
    subButt = st.button("Submit")

    if (st.session_state.debateForm == 'Thought Talk'):
        side = "Neutral"

    if (subButt and topicIn):
        st.session_state.debateTopic = topicIn
        st.session_state.debateSide = side
        nextPg()

elif st.session_state.page == 4:
    reTime = st.slider('How much research time do you want? (mins)', 0, 60, 15)
    # deTime = values = st.slider('How long will the debate time for each side last? (mins)', 0.5, 6.0, 1.5)
    timesButt = st.button("Submit")
    if (timesButt):
        st.session_state.rTime = reTime
        # st.session_state.dTime = deTime
        nextPg()

elif st.session_state.page == 5:
    # st.set_page_config()
    skipRTButt = st.button("Skip research time")
    st.write(st.session_state.debateTopic)

    ph = st.empty()
    N = st.session_state.rTime*60
    for secs in range(N,0,-1):
        if (skipRTButt):
            nextPg()
        mm, ss = secs//60, secs%60
        ph.metric("Research time remaining", f"{mm:02d}:{ss:02d}")
        time.sleep(1)
    nextPg()

elif st.session_state.page == 6:
    # --- Sidebar ---
    # with st.sidebar:
    #     ph = st.sidebar.empty()
    #     N = 5 * 60  # Set initial countdown duration (5 minutes)

    #     # Run the countdown timer
    #     for secs in range(N, 0, -1):
    #         mm, ss = secs // 60, secs % 60
    #         ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
    #         time.sleep(1)

    st.write(st.session_state.debateTopic)
    st.write("Your Side: ", st.session_state.debateSide)

    description = ""

    prompty = f"Debate me on the following topic: {st.session_state.debateTopic}. The debate format is a {st.session_state.debateForm}{description} My skill level is: {st.session_state.skillLvl}. I am arguing for the {st.session_state.debateSide} side. Respond appropriately to challenge me at this skill level. Argue only ONE point at a time and argue ONLY for the side opposing mine. Try not to answer in over 100 words, but address all portions of the opposing argument."

    chatter(model, prompty, st.session_state.debateSide)

    finishDebate = st.button("End Debate")
    if (finishDebate):
        nextPg()


elif st.session_state.page == 7:
    col1, col2, col3 = pg.columns(3)
    col2.image("judge.png", width=300)
    st.write("Here's how to improve:")
    genFeedback()
    
    #st.write(st.session_state.skillLvl, st.session_state.debateForm, st.session_state.debateSide, st.session_state.debateTopic, st.session_state.rTime, st.session_state.dTime)

# # # # # THOUGHT TALK PROMPT # # # # #
# Debate me on the following topic: ---. The debate format is a thought talk. In a thought talk, you can express any thoughts on the topic without picking any side. The other debater's skill level is: ---. Respond appropriately to challenge the debater at this skill level.
    
# # # # # CROSSFIRE PROMPT # # # # #
# Debate me on the following topic: ---. The debate format is a crossfire. In a crossfire, you are allowed to interrupt the other speaker and do not have to be very respectful. The other debater's skill level is: ---. You are arguing for the --- side. Respond appropriately to challenge the debater at this skill level.
    
# # # # # REGULAR PROMPT # # # # #
# Debate me on the following topic: ---. The debate format is regular. In a regular debate, you have --- time to debate and take turns arguing points. The other debater's skill level is: ---. You are arguing for the --- side. Respond appropriately to challenge the debater at this skill level.
