import asyncio
from random import randint

import streamlit as st

from engine.chat import ChatEngine
from frontend.footer import footer
from utils.constants import CHARACTER_AVATARS, CHARACTERS
from utils.message import reset_messages


@st.cache_resource(show_spinner=False)
def load_engine():
    with st.spinner(text="Loading the chat engine..."):
        return ChatEngine()


@st.cache_resource(show_spinner=False)
def load_avatars():
    return CHARACTER_AVATARS


st.set_page_config(page_title="Chat with you Nigerian hero",
                   page_icon="🇳🇬",
                   layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

with st.sidebar:
    st.title("Naija Echoes")
    st.info("This project was built as a way to remember all of our heroes")
    st.header("Choose your Nigerian Hero")
    if "char_id" not in st.session_state.keys():
        char_id = randint(0, len(CHARACTERS) - 1)
        st.session_state.char_id = char_id
    character = st.selectbox("Who do you want to chat with?", CHARACTERS,
                             on_change=reset_messages, index=st.session_state.char_id)
    st.write(f"You are currently chatting with {character}")
    footer()


async def main():
    st.title(f"Chat with {character} 🇳🇬")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"type": "ai", "data": "DEFAULT_MESSAGE"}]

    chat_engine: ChatEngine = load_engine()

    if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
        st.session_state.messages.append({"type": "human", "data": prompt})

    for message in st.session_state.messages:  # Display the prior chat messages
        if message["type"] == "human":
            avatar = "🫵🏽"
        else:
            avatar = load_avatars().get(character, "🇳🇬")
        with st.chat_message(message["type"], avatar=avatar):
            st.write(message["data"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["type"] != "ai":
        with st.chat_message("ai", avatar=load_avatars().get(character, "🇳🇬")):
            with st.spinner("Thinking..."):
                other_params = {"hero_name": character, "user_text": prompt}
                response = await chat_engine.chat(session=st.session_state, **other_params)
                st.write(response)
                message = {"type": "ai", "data": response}
                st.session_state.messages.append(message)


asyncio.run(main())
