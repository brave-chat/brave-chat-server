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


class Messages(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    sender: int = Column(ForeignKey("users.id"), index=True)
    receiver: int = Column(ForeignKey("users.id"), index=True)
    content: str = Column(String(1024), index=True)
    message_type: str = Column(String(10), index=True)
    media: str = Column(String(10))
