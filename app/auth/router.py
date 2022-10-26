from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
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
            "description": "Token value: {access_token: 'abcdefg12345token'"
            ", token_type: 'Bearer'}",
        },
        400: {"model": ResponseSchema, "description": "User not found!"},
        401: {"model": ResponseSchema, "description": "Invalid Credentials!"},
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    access_token = await login_user(form_data, session)
    return access_token


@router.post(
    "/auth/register",
    name="auth:register",
    response_model=Union[UserSchema, ResponseSchema],
    responses={
        201: {
            "model": UserCreate,
            "description": "Welcome to this blazingly fast chat app!",
        },
        400: {
            "model": ResponseSchema,
            "description": "User already signed up!",
        },
    },
)
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(get_db_transactional_session),
):
    results = await register_user(user, session)
    return results
