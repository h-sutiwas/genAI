import os

import requests
from dotenv import load_dotenv
import google.generativeai as genai

import streamlit as st

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure streamlit page
st.set_page_config(
    page_title='Chat with Kadmon AI',
    page_icon=':brain', # Emoji of brain
    layout='centered',  # Page layout option
)

# Set up Google Gemini AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-002")

# Function to translate roles between Gemini Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assignment"
    else:
        return user_role

# Initiative chat session in Streamlit if not already present
# Objective is to maintain all variables and other things in 
# the session so that when each click of button won't reset the web page
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the bot's name on the web page
st.title(":robot:" + " Kadmon AI - Chatbot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)
        
# Input field for user's messasge
user_prompt = st.chat_input("Ask Kadmon AI...")
if user_prompt:
    # Add user's message to chat and display it in a markdown format
    st.chat_message("user").markdown(user_prompt)
    
    # Send user's message to Gemini and get the message
    genai_response = st.session_state.chat_session.send_message(user_prompt)
    
    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(genai_response.text)