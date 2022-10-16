from sqlalchemy import Column, Integer, ForeignKey, String

from app.utils.mixins import Base, CommonMixin, TimestampMixin


class AccessTokens(Base, CommonMixin, TimestampMixin):
    user: int = Column(Integer, ForeignKey("users.id"), index=True)
    token: str = Column(String(120), index=True)


class BlackListedTokens(Base, CommonMixin, TimestampMixin):
    token: int = Column(Integer, ForeignKey("access_tokens.id"), index=True)
