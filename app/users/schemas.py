from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    Optional,
)

from app.users.models import (
    ChatStatus,
    UserRole,
    UserStatus,
)


class UserObjectSchema(BaseModel):
    id: int = Field(..., example=1)
    first_name: str = Field(..., example="First name.")
    last_name: str = Field(..., example="Last Name.")
    email: EmailStr = Field(..., example="testing@gmail.com")
    phone_number: Optional[str] = Field(..., example="123456789")
    bio: Optional[str] = Field(..., example="Your bio goes here.")
    chat_status: Optional[str] = Field(..., example=ChatStatus.online)
    user_status: str = Field(..., example=UserStatus.active)
    user_role: Optional[str] = Field(..., example=UserRole.regular)
    profile_picture: Optional[str] = Field(
        ...,
        example="{'preview': 'http://www.example.com/image', 'metaData': 'size, type...'}",
    )


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., example="testing@gmail.com")
    password: str = Field(..., example="A secure password goes here.")


class UpdateStatus(BaseModel):
    chat_status: str = Field(..., example=ChatStatus.online)


class PersonalInfo(BaseModel):
    first_name: str = Field(..., example="First name.")
    last_name: str = Field(..., example="Last Name.")
    bio: str = Field(..., example="Your bio goes here.")
    phone_number: str = Field(..., example="123456789")


class ResetPassword(BaseModel):
    old_password: str = Field(..., example="Your old password.")
    new_password: str = Field(..., example="Your new password.")
    confirm_password: str = Field(..., example="Your new password.")
