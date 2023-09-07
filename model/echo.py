from pydantic.v1 import Field

from model.base import EchoObject


class AssistantReply(EchoObject):
    """useful for replying to the user"""

    message: str = Field(..., description="a message from the assistant")
