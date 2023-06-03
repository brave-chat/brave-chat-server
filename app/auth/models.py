"""Auth models module."""

# conflict between isort and pylint
# pylint: disable=C0411
from enum import Enum

# pylint: disable=E0401
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from typing import (
    Optional,
    Union,
)

from app.utils.mixins import (
    Base,
    CommonMixin,
    TimestampMixin,
)


class TokenStatus(int, Enum):
    """
    Enum class to define token status.

    Args:
        ACTIVE (int) : An integer to indicate that the token is active.
        DISABLED (int) : An integer to indicate that the token has been disabled.
    """

    ACTIVE = 1
    DISABLED = 0


class AccessTokens(Base, CommonMixin, TimestampMixin):  # pylint: disable=R0903
    """
    The `access_tokens` model.

    Args:
        __table_args__ (dict) : SqlAlchemy configs to convert from COLUMNAR to ROWSTORE.
        user (int) : A user id foreign key value.
        token (str) : A token value.
        token_status (TokenStatus) : A token status.
    """

    __table_args__: dict[str, Union[str, list[str]]] = {
        "mysql_engine": "InnoDB",
        "prefixes": ["ROWSTORE", "REFERENCE"],
    }

    user: int = Column(ForeignKey("users.id"), index=True)
    token: str = Column(String(220), index=True)
    token_status: Optional[TokenStatus] = Column(Integer, nullable=True)
