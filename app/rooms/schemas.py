import datetime
from pydantic import (
    BaseModel,
    Field,
)
from typing import (
    Dict,
    List,
    Union,
)


class RoomCreate(BaseModel):
    room_name: str
    description: str


class RoomCreateResult(BaseModel):
    room_name: str
    members: List[str]
    conversation: List[str]
    active: str
    creation_date: datetime.datetime


class RoomGetALL(BaseModel):
    room_name: str
    members: List[Dict[str, Union[str, datetime.datetime]]]
    messages: List[Dict[str, Union[str, datetime.datetime]]]
    active: str
    creation_date: datetime.datetime


class LeaveRoom(BaseModel):
    room_name: str = Field(..., example="A room name to leave.")


class DeleteRoomConversation(BaseModel):
    room_name: str = Field(..., example="A room name to delete messages.")
