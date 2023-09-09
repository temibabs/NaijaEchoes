import asyncio
import logging
from random import randint

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from engine.chat import ChatEngine, StreamHandler
from frontend.footer import footer
from utils.constants import CHARACTER_AVATARS, CHARACTERS
from utils.message import reset_messages

logger = logging.getLogger(__name__)


def load_engine():
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
    st.info("This project was built as a way to celebrate our Nigerian heroes", icon="ℹ️")
    st.header("Choose your Nigerian Hero")
    if "char_id" not in st.session_state.keys():
        char_id = randint(0, len(CHARACTERS) - 1)
        st.session_state.char_id = char_id
    character = st.selectbox("Who do you want to chat with?", CHARACTERS,
                             on_change=reset_messages, index=st.session_state.char_id)
    st.write(f"You are currently chatting with {character}")
    footer()

screen_width = streamlit_js_eval(js_expressions='screen.width', want_output=True, key='SCR')
if screen_width is not None:
    if screen_width < 700:  # on mobile
        character = st.selectbox("Choose your hero:", CHARACTERS,
                                 on_change=reset_messages, index=st.session_state.char_id)


async def main():
    st.title(f"Chat with {character} 🇳🇬")

    chat_engine: ChatEngine = load_engine()

    if "messages" not in st.session_state.keys():
        with st.spinner(text=f"_setting up your chat with {character}..._"):
            intro = await chat_engine.get_intro(hero_name=character)
        st.session_state.messages = [{"type": "ai", "data": intro}]

    if prompt := st.chat_input("Message"):
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
            with st.spinner("_thinking..._"):
                other_params = {"hero_name": character, "user_text": prompt, "callback": StreamHandler()}
                try:
                    response = await chat_engine.chat(session=st.session_state, **other_params)
                except Exception as e:
                    logger.error(e)
                    response = await chat_engine.chat(session=st.session_state, **other_params)
                message = {"type": "ai", "data": response}
                st.session_state.messages.append(message)
    st.write(f"""<p style="font-size:11px;text-align:center;color:tomato;font-family:verdana;">
             This is not the real {character}, responses are AI-generated. Responses may also be inaccurate.
             If you accept, keep chatting
             </p>""",
             unsafe_allow_html=True)


asyncio.run(main())
