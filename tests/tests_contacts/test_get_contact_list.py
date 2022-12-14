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
async def test_get_contact_list(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    response = await client.get(
        url="/api/v1/contacts",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_200_OK
    assert len(dict_response["result"]) == 1
