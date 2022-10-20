from pydantic import (
    BaseModel,
)
from typing import (
    Optional,
)

from app.users.schemas import (
    UserObjectSchema,
)


class ContactCreate(BaseModel):
    user: str
    contact: str
    favourite: Optional[str]


class GetAllContactsResults(BaseModel):
    status_code: int
    result: list[UserObjectSchema]


class AddContact(BaseModel):
    contact: str
