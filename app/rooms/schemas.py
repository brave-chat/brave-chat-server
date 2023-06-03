import datetime
from pydantic import (
    BaseModel,
    EmailStr,
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


class BanUserRoom(BaseModel):
    room_name: str = Field(..., example="A room name.")
    email: EmailStr = Field(..., example="A user email to ban.")


class InviteUserRoom(BaseModel):
    room_name: str = Field(..., example="A room name.")
    email: EmailStr = Field(..., example="A user email to join.")
    invite_link: str = Field(..., example="An absolute URL to join the room.")


class InviteRoomLink(BaseModel):
    room_name: str = Field(..., example="A room name.")
    invite_link: str = Field(..., example="An absolute URL to join the room.")
