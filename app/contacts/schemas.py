from pydantic import (
    BaseModel,
)
from typing import (
    List,
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
    result: List[UserObjectSchema]


class AddContact(BaseModel):
    contact: str
