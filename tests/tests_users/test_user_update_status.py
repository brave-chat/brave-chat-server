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
)


@pytest.mark.anyio
async def test_user_successfull_status_update(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    json_data = {"chat_status": "offline"}
    response = await client.put(
        url="/api/v1/user",
        json=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_200_OK
