import datetime

import streamlit as st
from langchain import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.schema import HumanMessage, AIMessage

from engine.base import BaseEngine
from model.intro import Intro
from prompt.echo import ECHO_PROMPT
from prompt.intro import INTRO_PROMPT
from utils.hero import get_latest_news, get_relevant_info, get_sample_speeches

INTRO_SCHEMA = Intro.schema()


class StreamHandler(BaseCallbackHandler):
    def __init__(self, initial_text=""):
        self.container = st.empty()
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


class ChatEngine(BaseEngine):

    chat_chain = LLMChain(
        llm=ChatOpenAI(temperature=0,
                       model="gpt-3.5-turbo-0613",
                       streaming=True),
        prompt=ECHO_PROMPT
    )
    intro_chain = LLMChain(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        prompt=INTRO_PROMPT,
        llm_kwargs={
            "functions": [{
                "name": INTRO_SCHEMA["title"],
                "description": INTRO_SCHEMA["description"],
                "parameters": INTRO_SCHEMA
            }],
            "function_call": {"name": INTRO_SCHEMA["title"]}
        },
        output_parser=PydanticOutputFunctionsParser(pydantic_schema=Intro)
    )

    def _chat(self, session: dict, **kwargs) -> str:
        callbacks = [kwargs.pop("callback")]
        self.chat_chain.llm.callbacks = callbacks
        messages = []
        for message in session["messages"][-7:-1]:  # ignore last message as it is included in user_text
            _type = message["type"]
            if _type == "human":
                messages.append(HumanMessage(content=message["data"]))
            elif _type == "ai":
                messages.append(AIMessage(content=message["data"]))
            else:
                raise ValueError(f"Got unexpected message type: {_type}")
        params = {
            "history": messages,
            "relevant_info": get_relevant_info(hero_name=kwargs["hero_name"], query=kwargs["user_text"]),
            "sample_speech": get_sample_speeches()[kwargs["hero_name"]],
            "date_time": datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M:%S"),
            **kwargs,
        }
        reply = self.chat_chain.run(params)
        return reply

    async def get_intro(self, hero_name) -> str:
        params = {
            "hero_name": hero_name,
            "sample_speech": get_sample_speeches()[hero_name],
            "recent_news": get_latest_news()[hero_name],
            "date_time": datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M:%S")
        }
        reply = await self.intro_chain.arun(params)
        return reply.message

