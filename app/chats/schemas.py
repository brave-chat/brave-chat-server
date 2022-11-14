"""Chats Schemas module."""

# conflict between isort and pylint
# pylint: disable=C0411
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


class MessageCreate(BaseModel):
    """
    A Pydantic class that defines the message response schema for sending messages.

    Args:
        receiver (EmailStr) : The email of the message's recipient.
        content (str) : The content of the message.
        message_type (str) : The type of the message(e.g. 'text' or 'media').
        media (str) : A relative URL to the Deta drive.

    Example:
        >>> receiver = "testing@gmail.com"
        >>> content = "Hello there!"
        >>> message_type = "text"
        >>> media = ""
    """

    receiver: EmailStr = Field(
        ..., example="The recipient email for this message."
    )
    content: str = Field(..., example="The message text content.")
    message_type: str = Field(
        ..., example="Message type(e.g. 'text' or 'media')"
    )
    media: Optional[str] = Field(
        ...,
        example="A relative URL to the Deta drive.",
    )


class MessageCreateRoom(BaseModel):
    """
    A Pydantic class that defines the message response schema for sending messages in a room.

    Args:
        room (str) : A room name.
        content (str) : The content of the message.
        message_type (str) : The type of the message(e.g. 'text' or 'media').
        media (str) : A relative URL to the Deta drive.

    Example:
        >>> room = "nerds"
        >>> content = "Hello there!"
        >>> message_type = "text"
        >>> media = ""
    """

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
    """
    A Pydantic class that defines the message response schema for fetching all messages.

    Args:
        status_code (int) : A response status code.
        result (List[Dict[str, Any]]) : A secure password.
    """

    status_code: int = Field(..., example=200)
    result: List[Dict[str, Any]]


class DeleteChatMessages(BaseModel):
    """
    A Pydantic class that defines the message response schema for deleting messages.

    Args:
        contact (EmailStr) : The recipient email for the sent messages to be deleted.
    """

    contact: EmailStr = Field(
        ...,
        example="The recipient email for the sent messages to be deleted.",
    )
