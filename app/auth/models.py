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


class TokenStatus(int, Enum):
    active = 1
    disabled = 0


class AccessTokens(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    user: int = Column(ForeignKey("users.id"), index=True)
    token: str = Column(String(220), index=True)
    token_status: Optional[TokenStatus] = Column(Integer, nullable=True)
