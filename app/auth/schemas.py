from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.users.schemas import UserObjectSchema


class UserSchema(BaseModel):
    user: Optional[UserObjectSchema]
    token: Optional[dict[str, str]] = Field(
        ..., example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
    )
    status_code: int = Field(..., example=200)
    message: str = Field(..., example="You have successfully logged in!")


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., example="business@wiseai.dev")
    password: str = Field(..., example="SEc11r3P@ssw0rD")


class UserCreate(BaseModel):
    first_name: str = Field(..., example="Mahmoud")
    last_name: str = Field(..., example="Harmouch")
    email: str = Field(..., example="business@wiseai.dev")
    password: str = Field(..., example="SEc11r3P@ssw0rD")


class Token(BaseModel):
    access_token: str = Field(
        ..., example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
    )


class TokenData(BaseModel):
    email: Optional[str] = Field(..., example="business@wiseai.dev")


class ResponseSchema(BaseModel):
    status_code: int = Field(..., example=400)
    message: str = Field(..., example="Something went wrong!")
