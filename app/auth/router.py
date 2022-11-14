"""The auth router module."""

# conflict between isort and py
# pylint: disable=C0411
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

# pylint: disable=E0401
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from typing import (
    Union,
)

from app.auth.crud import (
    login_user,
    register_user,
)
from app.auth.schemas import (
    ResponseSchema,
    Token,
    UserCreate,
    UserSchema,
)
from app.utils.dependencies import (
    get_db_autocommit_session,
    get_db_transactional_session,
)

router = APIRouter(prefix="/api/v1")


@router.post(
    "/auth/login",
    response_model=Union[Token, ResponseSchema],
    status_code=200,
    name="auth:login",
    responses={
        201: {
            "model": Token,
            "description": "A response object contains a token object for a user"
            " e.g. Token value: {access_token: 'abcdefg12345token', token_type: 'Bearer'}",
        },
        400: {
            "model": ResponseSchema,
            "description": "A response object indicates that a user"
            " was not found!",
        },
        401: {
            "model": ResponseSchema,
            "description": "A response object indicates that invalid"
            " credentials were provided!",
        },
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    The login endpoint.

    Args:
        form_data (OAuth2PasswordRequestForm) : OAuth2 request form.
        session (AsyncSession) : An autocommit sqlalchemy session object.

    Returns:
        Token | ResponseSchema: return access token dict, or response schema object.
    """
    access_token = await login_user(form_data, session)
    return access_token


@router.post(
    "/auth/register",
    name="auth:register",
    response_model=Union[UserSchema, ResponseSchema],
    responses={
        201: {
            "model": UserCreate,
            "description": "A response object that contains a welcome message"
            " on a successfull login!",
        },
        400: {
            "model": ResponseSchema,
            "description": "A response object to indicate that a user has already signed up"
            " using this email!",
        },
    },
)
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(get_db_transactional_session),
):
    """
    The register endpoint.

    Args:
        user (UserCreate) : A UserCreate schema object.
        session (AsyncSession) : A transactional sqlalchemy session object.

    Returns:
        UserCreate | ResponseSchema: return UserCreate or ResponseSchema object.
    """
    results = await register_user(user, session)
    return results
