import pytest

from fastapi import (
    FastAPI,
)
from httpx import (
    AsyncClient,
)
import json
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)


@pytest.mark.anyio
async def test_user_successful_registration(
    fastapi_app: FastAPI, client: AsyncClient
) -> None:
    json_data = {
        "first_name": "Mahmoud",
        "last_name": "Harmouch",
        "email": "business@wiseai.dev",
        "password": "SEc11r3P@ssw0rD",
    }
    response = await client.post(
        url="/api/v1/auth/register",
        json=json_data,
        headers={"Content-Type": "application/json"},
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_201_CREATED


@pytest.mark.anyio
async def test_user_already_signed_up(
    fastapi_app: FastAPI, client: AsyncClient
) -> None:
    json_data = {
        "first_name": "Mahmoud",
        "last_name": "Harmouch",
        "email": "business@wiseai.dev",
        "password": "SEc11r3P@ssw0rD",
    }
    response = await client.post(
        url="/api/v1/auth/register",
        json=json_data,
        headers={"Content-Type": "application/json"},
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_400_BAD_REQUEST
