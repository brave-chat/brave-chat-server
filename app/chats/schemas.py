from pydantic import (
    BaseModel,
    Field,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


class MessageCreate(BaseModel):
    receiver: str = Field(..., example="The recipient email for this message.")
    content: str = Field(..., example="The message text content.")
    message_type: str = Field(
        ..., example="Message type(e.g. 'text' or 'media')"
    )
    media: Optional[str] = Field(
        ...,
        example="A dictionary that contains media url, type. (e.g. {'preview': "
        "'http://www.example.com/image', 'metaData': 'size, type...'})",
    )


class MessageCreateRoom(BaseModel):
    room: str = Field(
        ..., example="A unique room name(e.g. 'nerds'). Case Sensitive."
    )
    content: str = Field(..., example="The message text content.")
    message_type: str = Field(
        ..., example="Message type(e.g. 'text' or 'media')"
    )
    media: Optional[str] = Field(
        ..., example="A dictionary that contains media url, type..."
    )


class GetAllMessageResults(BaseModel):
    status_code: int = Field(..., example=200)
    result: List[Dict[str, Any]]


class DeleteChatMessages(BaseModel):
    contact: str = Field(
        ...,
        example="The recipient email for these messages to delete the sent ones.",
    )
