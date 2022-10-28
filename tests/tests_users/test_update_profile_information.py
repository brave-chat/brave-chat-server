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
async def test_user_successfull_profile_info_update(
    fastapi_app: FastAPI, client: AsyncClient, token: str
) -> None:
    json_data = {
        "first_name": "Mahmoud",
        "last_name": "Harmouch",
        "bio": "A Full Stack Developer.",
        "phone_number": "99999999",
    }
    response = await client.put(
        url="/api/v1/user/profile",
        json=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    dict_response = json.loads(response.content.decode())
    assert dict_response["status_code"] == HTTP_200_OK
