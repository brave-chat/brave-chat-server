import pytest

from fastapi import (
    FastAPI,
)
from httpx import (
    AsyncClient,
)
import json
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)


@pytest.mark.anyio
async def test_user_successful_login(
    fastapi_app: FastAPI, client: AsyncClient
) -> None:
    email = "test@example.com"
    password = "test"
    response = await client.post(
        url="/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    dict_response = json.loads(response.content.decode())
    assert "access_token" in dict_response


@pytest.mark.anyio
async def test_user_login_when_credential_part_does_not_match(
    fastapi_app: FastAPI, client: AsyncClient
) -> None:
    email = "test@test.com"
    password = "invalid"
    response = await client.post(
        url="/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_user_login_does_not_exist(
    fastapi_app: FastAPI, client: AsyncClient
) -> None:
    email = "invalid@test.com"
    password = "invalid"
    response = await client.post(
        url="/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_400_BAD_REQUEST
