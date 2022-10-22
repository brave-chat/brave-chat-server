from sqlalchemy import (
    Column,
    ForeignKey,
    String,
)

from app.utils.mixins import (
    Base,
    CommonMixin,
    TimestampMixin,
)


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
