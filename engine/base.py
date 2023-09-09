from abc import ABCMeta, abstractmethod

from langchain import LLMChain
from pydantic.v1 import BaseModel


class BaseEngine(BaseModel, metaclass=ABCMeta):

    chat_chain: LLMChain

    async def chat(self, session: dict, **kwargs) -> str:
        return self._chat(session, **kwargs)

    @abstractmethod
    def _chat(self, session: dict, **kwargs) -> str:
        """"""
