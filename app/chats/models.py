"""Chats models module."""

# conflict between isort and pylint
# pylint: disable=C0411
from enum import Enum
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from typing import (
    Optional,
)

from app.utils.mixins import (
    Base,
    CommonMixin,
    TimestampMixin,
)


class MessageStatus(int, Enum):
    """
    Enum class to define a message status.

    Args:
        READ (int) : A constant integer to indicate that the recipient read the message.
        NOT_READ (int) : A constant integer to indicate that the recipient didn't read the message.
    """

    READ = 0
    NOT_READ = 1


class Messages(Base, CommonMixin, TimestampMixin):  # pylint: disable=R0903
    """
    The `messages` model.

    Args:
        __table_args__ (dict) : SqlAlchemy configs to convert from COLUMNAR to ROWSTORE.
        sender (int) : A user id foreign key value for the sender of the message.
        receiver (int) : A user id foreign key value for the recipient of the message.
        room (int) : A room id foreign key value of the message.
        content (str) : The content of the message.
        status (int) : The status of the message(e.g. read or not read).
        message_type (str) : The message type(e.g. 'text' or 'media').
        media (str) : A relative URL to the location of the image on the Deta drive.
    """

    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    sender: int = Column(ForeignKey("users.id"), index=True)
    receiver: int = Column(ForeignKey("users.id"), index=True)
    room: int = Column(ForeignKey("rooms.id"), index=True, default=None)
    content: str = Column(String(1024), index=True)
    status: int = Column(
        Integer, index=True, default=MessageStatus.NOT_READ.value
    )
    message_type: str = Column(String(10), index=True)
    media: Optional[str] = Column(String(220), nullable=True)
