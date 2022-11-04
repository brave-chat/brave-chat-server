from enum import Enum
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from typing import (
    Any,
    Optional,
)

from app.utils.mixins import (
    Base,
    CommonMixin,
    TimestampMixin,
)


class MessageStatus(int, Enum):
    read = 0
    not_read = 1


class Messages(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    sender: int = Column(ForeignKey("users.id"), index=True)
    receiver: int = Column(ForeignKey("users.id"), index=True)
    room: int = Column(ForeignKey("rooms.id"), index=True, default=None)
    content: str = Column(String(1024), index=True)
    status: int = Column(
        Integer, index=True, default=MessageStatus.not_read.value
    )
    message_type: str = Column(String(10), index=True)
    media: Optional[Any] = Column(String(220), nullable=True)
