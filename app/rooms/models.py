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


class UserStatus(int, Enum):
    banned = 1
    not_banned = 0


class UserRole(int, Enum):
    admin = 1
    not_admin = 0


class Rooms(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    room_name: int = Column(String(20), index=True)
    description: str = Column(String(60))


class RoomMembers(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    room: int = Column(ForeignKey("rooms.id"), index=True)
    member: int = Column(ForeignKey("users.id"), index=True)
    banned: Optional[UserStatus] = Column(Integer, index=True)
    admin: Optional[UserRole] = Column(Integer, index=True)
