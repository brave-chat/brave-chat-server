"""Auth Schemas module."""

# conflict between isort and pylint
# pylint: disable=C0411
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    Dict,
    Optional,
)

from app.users.schemas import (
    UserObjectSchema,
)


class UserSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for registration.

    Args:
        user (UserObjectSchema) : A user schema object to hide users passwords.
        token (str) : Token value.
        status_code (str) : A response status code.
        message (str) : A message to indicate whether or not the login was successful.

    Example:
        >>> user = UserObjectSchema(
            id=1,
            first_name="First Name.",
            last_name="Last Name.",
            email="testing@gmail.com",
            phone_number="123456789",
            bio="Your bio goes here.",
            chat_status="online",
            user_status=1,
            user_role="regular",
            profile_picture="{'preview': 'http://www.example.com/image',"
            "'metaData': 'size, type...'}",
        )
        >>> token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
        >>> status_code = 200
        >>> message = "You have registered successfully!"
    """

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
            profile_picture="{'preview': 'http://www.example.com/image',"
            "'metaData': 'size, type...'}",
        ),
    )
    token: Optional[Dict[str, str]] = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )
    status_code: int = Field(
        ...,
        example="A response status code. (e.g. 200 on a successful attempt.)",
    )
    message: str = Field(
        ...,
        example="A message to indicate whether or not the login was successful!",
    )


class UserLoginSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for logging in.

    Args:
        email (str) : User email address.
        password (str) : A secure password.

    Example:
        >>> email = "testing@gmail.com"
        >>> password = "S3C11R3P@55W0rD"
    """

    email: EmailStr = Field(..., example="Your email address to log in.")
    password: str = Field(..., example="A secure password goes here.")


class UserCreate(BaseModel):
    """
    A Pydantic class that defines the user schema for sign up.

    Args:
        first_name (str) : User first name.
        last_name (str) : User last name.
        email (str) : User email address.
        password (str) : A secure password.

    Example:
        >>> first_name = "first name"
        >>> last_name = "last name"
        >>> email = "test@test.com"
        >>> password = "S3C11R3P@55W0rD"
    """

    first_name: str = Field(..., example="Your first name.")
    last_name: str = Field(..., example="Your last name.")
    email: str = Field(
        ..., example="Your email address to register into the app."
    )
    password: str = Field(..., example="A secure password goes here.")


class Token(BaseModel):
    """
    A Pydantic class that defines the Token schema.

    Args:
        access_token (str) : A token value.

    Example:
        >>> access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
    """

    access_token: str = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )


class TokenData(BaseModel):
    """
    A Pydantic class that defines a Token schema to return the email address.

    Args:
        email (str) : User email address.

    Example:
        >>> email = "test@test.com"
    """

    email: Optional[str] = Field(..., example="Your email address.")


class ResponseSchema(BaseModel):
    """
    A Pydantic class that defines a Response schema object.

    Args:
        status_code (int) : Response status code.
        message (str) : Response message.

    Example:
        >>> status_code = 200
        >>> message = "You have logged in successfully!"
    """

    status_code: int = Field(
        ...,
        example=400,
    )
    message: str = Field(
        ...,
        example="A message to indicate that the request was not successful!",
    )
