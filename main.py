import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def init():
    st.set_page_config(
        page_title="Your own ChatGPT",
        page_icon="🤖"
    )

def main():
    init()

    st.sidebar.title("API Settings")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
    clear_button = st.sidebar.button("CLEAR API KEY")

    if clear_button:
        os.environ["OPENAI_API_KEY"] = ""
        st.sidebar.success("API Key cleared. Please refresh the page.")

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.sidebar.success("API Key set successfully. Please refresh the page.")

    # Reload the environment variables after setting them
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        st.error("OPENAI_API_KEY is not set.")
        st.stop()

    chat = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    st.header("Your own ChatGPT 🤖")

    with st.sidebar:
        user_input = st.chat_input("Your message:", key="user_input")

        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))

            with st.spinner("Thinking...."):
                response = chat(st.session_state.messages)

            st.session_state.messages.append(AIMessage(content=response.content))

            # Write the chat messages to a text file
            with open("chat_history.txt", "a+") as file:
                file.write(f"User: {user_input}\n")
                file.write(f"AI: {response.content}\n")

    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')

if __name__ == '__main__':
    main()
