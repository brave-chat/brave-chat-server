from sqlalchemy import (
    Column,
    ForeignKey,
)

from app.utils.mixins import (
    Base,
    CommonMixin,
    TimestampMixin,
)


class Contacts(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    user: int = Column(ForeignKey("users.id"), index=True)
    contact: int = Column(ForeignKey("users.id"), index=True)
