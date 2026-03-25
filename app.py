import streamlit as st

import json

def load_data():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open("users.json", "w") as f:
         json.dump(data, f, indent=4)

if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = ""


#-------------------------------------------------Home Page-------------------------------------------------------------------------------------------

if st.session_state.page == "home":

    st.title("Home Page")

    if st.button("signup"):
        st.session_state.page = "signup"
        st.rerun()

    if st.button("login"):
        st.session_state.page = "login"
        st.rerun()

 #------------------------------------------------SignUp Page -----------------------------------------------------------------------------------------

if st.session_state.page == "signup":

    st.title("Enter Details to Signup") 

    user_name = st.text_input("username")
    password = st.text_input("passowrd", type="password")

    if st.button("create account"):

        if user_name and password:
            data = load_data()

            if user_name in data:
                st.error("username already taken")
            else:
                data[user_name] = password 
                save_data(data)  
                st.session_state.page = "dashboard"
                st.session_state.user = user_name
                st.rerun()   
        else:
            st.error("Fields cannot be empty") 

    if st.button("back"):
       st.session_state.page = "home"
       st.session_state.user = ""


#------------------------------------------------Login Page -----------------------------------------------------------------------------------------

if st.session_state.page == "login":

    st.title("Enter Details to Login")

    user_name = st.text_input("username")
    password = st.text_input("password", type="password")

    if st.button("login"):     
       if user_name and password:
          
          data = load_data()
          if password == data[user_name]:
             
             st.session_state.user = user_name
             st.session_state.page = "dashboard"
             st.rerun()
          else:
             st.error("Incorrect Details")
       else:
           st.error("Fields cannot be empty")

    if st.button("back"):
       st.session_state.page = "home"
       st.session_state.user = ""


#------------------------------------------------DashBoard Page -----------------------------------------------------------------------------------------
import os 

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=api_key)

# if st.session_state.page == "dashboard":
#     st.write(f"Welcome {st.session_state.user}")

#     if "messages" not in st.session_state:
#         st.session_state.messages = []
        
#     for msg in st.session_state.messages:
#         role = "user" if msg.type == "human" else "assistant"
#         with st.chat_message(role):
#              st.write(msg.content)
        
#         user_input = st.text_input("Type...")

#         if user_input:
#            st.session_state.messages.append(HumanMessage(content=user_input))

#            response = model.invoke(st.session_state.messages)

#            st.session_state.messages.append(AIMessage(content=response.content))

#            st.rerun()

#     if st.button("back"):
#        st.session_state.page = "home"
#        st.session_state.user = ""
#        st.rerun()



if st.session_state.page == "dashboard":
    st.write(f"Welcome {st.session_state.user}")

    # Initialize messages if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # 1. ALWAYS display existing messages first (Outside the input logic)
    for msg in st.session_state.messages:
        role = "user" if msg.type == "human" else "assistant"
        with st.chat_message(role):
            st.write(msg.content)

    # 2. Use st.chat_input instead of text_input (It looks better and stays at the bottom)
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Show user message immediately
        # with st.chat_message("user"):
        #     st.write(user_input)
        
        # Add to state
        st.session_state.messages.append(HumanMessage(content=user_input))

        # Get AI Response
        response = model.invoke(st.session_state.messages)
        
        # Show AI message immediately
        # with st.chat_message("assistant"):
        #     st.write(response.content)
            
        st.session_state.messages.append(AIMessage(content=response.content))
        
        # Rerun to keep state synced
        st.rerun()

    # Back button should be at the very bottom or in a sidebar
    if st.sidebar.button("Logout"):
        st.session_state.page = "home"
        st.session_state.user = ""
        st.session_state.messages = [] # Clear chat on logout
        st.rerun()