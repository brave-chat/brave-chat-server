import datetime
from pydantic import (
    BaseModel,
    Field,
)
from typing import (
    Any,
    Optional,
)


class MessageCreate(BaseModel):
    receiver: str = Field(..., example="business@wiseai.dev")
    content: str = Field(..., example="Hello World!")
    message_type: str = Field(..., example="text")
    media: Optional[str] = Field(..., example="")
