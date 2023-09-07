import datetime

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.schema import HumanMessage, AIMessage

from engine.base import BaseEngine
from model.intro import Intro
from prompt.echo import ECHO_PROMPT
from prompt.intro import INTRO_PROMPT
from utils.hero import get_latest_news, get_relevant_info

INTRO_SCHEMA = Intro.schema()


class ChatEngine(BaseEngine):

    chat_chain = LLMChain(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
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

    async def _chat(self, session: dict, **kwargs) -> str:

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
            "relevant_info": await get_relevant_info(hero_name=kwargs["hero_name"], query=kwargs["user_text"]),
            "date_time": datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M:%S"),
            **kwargs,
        }
        reply = await self.chat_chain.arun(params)
        return reply

    async def get_intro(self, hero_name) -> str:
        params = {
            "hero_name": hero_name,
            "character_info": "BLANK",
            "recent_news": get_latest_news()[hero_name],
            "date_time": datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M:%S")
        }
        reply = await self.intro_chain.arun(params)
        return reply.message

