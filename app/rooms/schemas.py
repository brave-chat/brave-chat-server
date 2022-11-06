import datetime
from pydantic import (
    BaseModel,
    Field,
)
from typing import (
    Union,
)


class RoomCreate(BaseModel):
    join: int
    room_name: str
    description: str


class RoomCreateResult(BaseModel):
    room_name: str
    members: list[str]
    conversation: list[str]
    active: str
    creation_date: datetime.datetime


class RoomGetALL(BaseModel):
    room_name: str
    members: list[dict[str, Union[str, datetime.datetime]]]
    messages: list[dict[str, Union[str, datetime.datetime]]]
    active: str
    creation_date: datetime.datetime


class LeaveRoom(BaseModel):
    room_name: str = Field(..., example="A room name to leave.")


class DeleteRoomConversation(BaseModel):
    room_name: str = Field(..., example="A room name to delete messages.")
