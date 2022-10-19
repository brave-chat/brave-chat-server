from sqlalchemy import (
    BIGINT,
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    backref,
    relationship,
)

from app.utils.mixins import (
    Base,
    CommonMixin,
    TimestampMixin,
)


class AccessTokens(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    user: int = Column(ForeignKey("users.id"), index=True)
    token: str = Column(String(220), index=True)


class BlackListedTokens(Base, CommonMixin, TimestampMixin):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    token: int = Column(ForeignKey("access_tokens.id"), index=True)