from typing import Union

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.crud import login_user, register_user
from app.auth.schemas import ResponseSchema, Token, UserCreate, UserSchema

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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await login_user(form_data)
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
async def register(user: UserCreate):
    results = await register_user(user)
    return results
