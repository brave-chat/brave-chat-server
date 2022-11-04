from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    Optional,
)

from app.users.schemas import (
    UserObjectSchema,
)


class UserSchema(BaseModel):
    user: Optional[UserObjectSchema] = Field(
        ...,
        example=UserObjectSchema(
            id=1,
            first_name="First Name.",
            last_name="Last Name.",
            email="testing@gmail.com",
            phone_number="123456789",
            bio="Your bio goes here.",
            chat_status="online",
            user_status=1,
            user_role="regular",
            profile_picture="{'preview': 'http://www.example.com/image', 'metaData': 'size, type...'}",
        ),
    )
    token: Optional[dict[str, str]] = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )
    status_code: int = Field(
        ...,
        example="A response status code. (e.g. 200 on a successfull attempt.)",
    )
    message: str = Field(
        ...,
        example="A message to indicate whether or not the login was successfull!",
    )


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., example="Your email address to log in.")
    password: str = Field(..., example="A secure password goes here.")


class UserCreate(BaseModel):
    first_name: str = Field(..., example="Your first name.")
    last_name: str = Field(..., example="Your last name.")
    email: str = Field(
        ..., example="Your email address to register into the app."
    )
    password: str = Field(..., example="A secure password goes here.")


class Token(BaseModel):
    access_token: str = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )


class TokenData(BaseModel):
    email: Optional[str] = Field(..., example="Your email address.")


class ResponseSchema(BaseModel):
    status_code: int = Field(
        ...,
        example=400,
    )
    message: str = Field(
        ...,
        example="A message to indicate that the request was not successfull!",
    )
