from pydantic.v1 import Field

from model.base import EchoObject


class Intro(EchoObject):
    """useful for introducing yourself"""

    mannerism: str = Field(..., description="your mannerism in one word")
    mood: str = Field(..., description="your mood in one word based on recent news")
    message: str = Field(..., description="a message from the assistant")
