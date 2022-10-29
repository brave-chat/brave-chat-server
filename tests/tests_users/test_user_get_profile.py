import pytest

from fastapi import (
    FastAPI,
)
from httpx import (
    AsyncClient,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)


@pytest.mark.anyio
async def test_unable_to_get_current_profile_with_wrong_jwt_prefix(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    response = await client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Invalid {token}"},
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_authorized_get_current_profile(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    response = await client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTP_200_OK
