from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.schema import messages_from_dict, HumanMessage, AIMessage

from engine.base import BaseEngine
from model.echo import AssistantReply
from prompt.echo import ECHO_PROMPT


REPLY_SCHEMA = AssistantReply.schema()


class ChatEngine(BaseEngine):

    chat_chain = LLMChain(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        prompt=ECHO_PROMPT,
        llm_kwargs={
            "functions": [{
                "name": REPLY_SCHEMA["title"],
                "description": REPLY_SCHEMA["description"],
                "parameters": REPLY_SCHEMA
            }],
            "function_call": {"name": REPLY_SCHEMA["title"]}
        },
        output_parser=PydanticOutputFunctionsParser(pydantic_schema=AssistantReply)
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
            **kwargs,
        }
        reply = self.chat_chain.run(params)
        return reply.message
