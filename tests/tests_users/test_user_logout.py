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
    HTTP_401_UNAUTHORIZED,
)


@pytest.mark.anyio
@pytest.mark.skip(reason="Weird SQLAlchemy behaviour")
async def test_user_successfull_logout(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    response = await client.get(
        "/api/v1/user/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTP_200_OK

    response = await client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
