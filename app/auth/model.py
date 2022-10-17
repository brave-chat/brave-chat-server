from sqlalchemy import Column, BIGINT, ForeignKey, String

from app.utils.mixins import Base, CommonMixin, TimestampMixin
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

class AccessTokens(Base, CommonMixin, TimestampMixin):
    user: int = Column(ForeignKey("users.id"), index=True)
    token: str = Column(String(220), index=True)


class BlackListedTokens(Base, CommonMixin, TimestampMixin):
    token: int = Column(ForeignKey("access_tokens.id"), index=True)