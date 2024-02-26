import streamlit as st
import streamlit as stChat
import google.generativeai as genai
from dotenv import main
import os

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
    return model.generate_content("Generate only ONE debate topic. Do NOT generate more than one debate topic. Only return the topic with NO other numbers or text. Return in the format 'Resolved:' ")

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
        nextPg()
    elif (midButt):
        st.session_state.skillLvl = 2
        nextPg()
    elif (expButt):
        st.session_state.skillLvl = 3
        nextPg()

elif st.session_state.page == 2:
    col1, col2, col3 = pg.columns(3)
    debateFormButt = col2.button("Submit")
    option = col2.selectbox(
    'What debate format would you like?',
    ('', 'Standard', 'Crossfire', 'Thought Talk'))
    if (option == 'Standard'):
        col2.write("This is normal debating")
    elif (option == 'Crossfire'):
        col2.write("This is fiery debating")
    elif (option == 'Thought Talk'):
        col2.write("This is relaxed debating")
    # if (option == '')
    if (debateFormButt):
        if (option == ''):
            col2.write("Pick one of the options")
        else: 
            st.session_state.debateForm = option
            nextPg()

elif st.session_state.page == 3:
    st.markdown("<h1 style='text-align: center; color: white;'>Topic</h1>", unsafe_allow_html=True)
    topicIn = st.text_input("Enter a topic of your choice")
    randButt = st.button("Randomize")
    if (randButt):
        topicIn = genTopic().text
        st.write(topicIn)
    side = st.radio(
    "What side will you argue",
    ["Pro", "Con", "Either"])
    subButt = st.button("Submit")
    if (subButt):
        st.session_state.debateTopic = topicIn
        st.session_state.debateSide = side
        nextPg()

elif st.session_state.page == 4:
    reTime = st.slider('How much research time do you want? (mins)', 0, 60, 0)
    deTime = st.slider('How long will the debate time for each side last? (secs)', 30, 360, 30)
    timesButt = st.button("Submit")
    if (timesButt):
        st.session_state.rTime = reTime
        st.session_state.dTime = deTime
        nextPg()

elif st.session_state.page == 5:
    arg = st.text_area("Argue your side!")
    finishDebate = st.button("End Debate")
    if (finishDebate):
        nextPg()


elif st.session_state.page == 6:
    col1, col2, col3 = pg.columns(3)
    col2.image("judge.png", width=300)
    st.write("heres how to improve:")
    st.write(st.session_state.skillLvl, st.session_state.debateForm, st.session_state.debateSide, st.session_state.debateTopic, st.session_state.rTime, st.session_state.dTime)

# if (startButton):y5
#     pg.empty()

#     col1, col2, col3 = pg.columns(3)
#     option = col2.selectbox(
#     'What debate format would you like?',
#     ('Standard', 'Crossfire', 'Thought Talk')
#     )


# img = Image.open("ai_debate_logo.png")
# st.button(st.image(img))
