from enum import Enum
from pydantic import (
    EmailStr,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from typing import (
    Optional,
)

from app.utils.full_text_search import (
    Fulltext,
)
from app.utils.mixins import (
    Base,
    CommonMixin,
    TimestampMixin,
)


class ChatStatus(str, Enum):
    online = "online"
    offline = "offline"
    busy = "busy"
    dont_disturb = "don't disturb"


class UserStatus(int, Enum):
    active = 1
    disabled = 0


class UserRole(str, Enum):
    regular = "regular"
    admin = "admin"


class Users(Base, CommonMixin, TimestampMixin):
    __table_args__ = (Fulltext("first_name, last_name, email"),)

    first_name: str = Column(String(20), index=True)
    last_name: str = Column(String(20), index=True)
    email: EmailStr = Column(String(50), index=True)
    password: str = Column(String(120), index=True)
    phone_number: str = Column(String(20), nullable=True)
    bio: Optional[str] = Column(String(60), nullable=True)
    profile_picture: Optional[str] = Column(String(220), nullable=True)
    chat_status: Optional[ChatStatus] = Column(String(20), nullable=True)
    user_status: Optional[UserStatus] = Column(
        Integer, index=True, nullable=True
    )
    user_role: Optional[UserRole] = Column(String(20), nullable=True)
