import streamlit as st
from model import connector


st.title("Chatbot with Ranger API")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

openapi_key = st.sidebar.text_input("Enter Your Open API Key", type="password",placeholder="sk-j*****************************") 
if len(openapi_key) < 1:
    st.sidebar.markdown(f"<div style='background-color:white; color: red; font-size: 15px; padding:0px; margin-top: -10px; margin-bottom: 20px; border-radius: 10px;'>*OpenAi API key is required</div>", unsafe_allow_html=True)

username = st.sidebar.text_input("Ranger Username", type="default",value="admin") 
if len(username) < 1:
    st.sidebar.markdown(f"<div style='background-color:white; color: red; font-size: 15px; padding:0px; margin-top: -10px; margin-bottom: 20px; border-radius: 10px;'>*Username is required</div>", unsafe_allow_html=True)

password = st.sidebar.text_input("Ranger Password", type="password",placeholder="********")
if len(password) < 1:
    st.sidebar.markdown(f"<div style='background-color:white; color: red; font-size: 15px; padding:0px; margin-top: -10px; margin-bottom: 20px; border-radius: 10px;'>*Password is required</div>", unsafe_allow_html=True)

with st.form(key="my_form",clear_on_submit=True):
    text = st.text_area("Enter your text here",placeholder="How Can I Help You!")
    st.info(text)
    if st.form_submit_button("Submit"):
        result = connector(openapi_key,username, password,text)
        st.markdown(f"<div style='background-color:#D4F1F4; padding:10px; margin-bottom: 20px; border-radius: 10px;'>{result}</div>", unsafe_allow_html=True)