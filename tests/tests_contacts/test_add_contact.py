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
@pytest.mark.xfail
async def test_add_contact_successfull(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    json_data = {"contact": "test1@example.com"}
    response = await client.post(
        url="/api/v1/contact",
        json=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_201_CREATED


@pytest.mark.anyio
async def test_add_contact_non_existing_user(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    json_data = {"contact": "123@example.com"}
    response = await client.post(
        url="/api/v1/contact",
        json=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_add_contact_cant_add_yourself(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    json_data = {"contact": "test@example.com"}
    response = await client.post(
        url="/api/v1/contact",
        json=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_add_contact_already_added(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    json_data = {"contact": "test1@example.com"}
    response = await client.post(
        url="/api/v1/contact",
        json=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_201_CREATED
    response = await client.post(
        url="/api/v1/contact",
        json=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_400_BAD_REQUEST
