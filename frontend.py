## Step 1: Setup the streamlit
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/ask"
# http://127.0.0.1:8000/docs#/default/ask_ask_post
st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


## Step 2: User is able to ask question

user_input = st.chat_input("What's on your mind today ?")
if user_input:
    ## append the user message
    st.session_state.chat_history.append({"role":"user" , "content":user_input})


    ## ai agent
    response = requests.post(BACKEND_URL , json={"message":user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": f'{response.json()["response"]} WITH TOOL: [{response.json()["tool_called"]}]'})


# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])