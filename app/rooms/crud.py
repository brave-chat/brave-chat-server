import datetime
import logging
from typing import (
    Optional,
)

from app.auth.crud import (
    find_existed_user,
)
from app.chats.crud import (
    send_new_message,
)
from app.chats.schemas import (
    MessageCreateRoom,
)
from app.users.schemas import (
    UserObjectSchema,
)
from app.utils.session import (
    database,
)

logger = logging.getLogger(__name__)


async def find_existed_room(room_name: str):
    query = """
        SELECT
          *
        FROM
          rooms
        WHERE
          room_name = :room_name
    """
    values = {"room_name": room_name}
    return await database.fetch_one(query, values=values)


async def find_existed_user_in_room(user_id: int, room_id: int):
    query = """
        SELECT
          *
        FROM
          room_members
        WHERE
          room = :room_id
        AND
          member = :user_id
    """
    values = {"room_id": room_id, "user_id": user_id}
    return await database.fetch_one(query, values=values)


async def create_room(room_name: int, description: str):
    query = """
        INSERT INTO rooms (
          room_name,
          description,
          creation_date
        )
        VALUES (
          :room_name,
          :description,
          :creation_date
        )
    """
    values = {
        "room_name": room_name,
        "description": description,
        "creation_date": datetime.datetime.utcnow(),
    }
    return await database.fetch_one(query, values=values)


async def join_room(user_id: int, room_id: int):
    query = """
        INSERT INTO room_members (
          room,
          member,
          creation_date
        )
        VALUES (
          :room,
          :member,
          :creation_date
        )
    """
    values = {
        "room": room_id,
        "member": user_id,
        "creation_date": datetime.datetime.utcnow(),
    }
    return await database.execute(query, values=values)


async def create_assign_new_room(user_id: int, room_obj):
    room = await find_existed_room(room_obj.room_name)
    if not room:
        await create_room(room_obj.room_name, room_obj.description)
        logger.info(f"Creating room `{room_obj.room_name}`.")
        room = await find_existed_room(room_obj.room_name)
        user = await find_existed_user_in_room(user_id, room.id)
        if user:
            logger.info(f"`{user_id}` has already joined this room!")
            results = {
                "status_code": 400,
                "message": "You have already joined room"
                f"{room_obj.room_name}!",
            }
        else:
            await join_room(user_id, room.id)
            logger.info(
                f"Adding {user_id} to room `{room_obj.room_name}` as a member."
            )
            results = {
                "status_code": 200,
                "message": f"You have joined room {room_obj.room_name}!",
            }
        return results

    else:
        user = await find_existed_user_in_room(user_id, room.id)
        print(user)
        if user:
            logger.info(f"`{user_id}` has already joined this room!")
            results = {
                "status_code": 400,
                "message": "You have already joined room "
                f"{room_obj.room_name}!",
            }
        else:
            await join_room(user_id, room.id)
            logger.info(
                f"Adding {user_id} to room `{room_obj.room_name}` as a member."
            )
            results = {
                "status_code": 200,
                "message": f"You have joined room {room_obj.room_name}!",
            }
        return results


async def get_room_conversations(room_name: str, sender_id: int):
    room = await find_existed_room(room_name)
    if not room:
        return {
            "status_code": 400,
            "message": "Room not found!",
        }
    query = """
        SELECT
            id,
            content,
            CASE
                WHEN sender = :sender_id THEN "sent"
                ELSE "received"
            END as type,
            media,
            creation_date
        FROM
            messages
        WHERE
          room = :room_id
        ORDER BY
          creation_date
    """
    values = {"room_id": room.id, "sender_id": sender_id}
    messages_sent_received = await database.fetch_all(query, values=values)
    results = {
        "status_code": 200,
        "result": messages_sent_received,
    }
    return results


async def send_new_room_message(
    sender: UserObjectSchema, request: MessageCreateRoom
):
    # Check for empty message
    if not request.content:
        return {
            "status_code": 400,
            "message": "You can't send an empty message!",
        }
    room = await find_existed_room(request.room)
    if not room:
        return {
            "status_code": 400,
            "message": "You can't send a message to a non existing room!",
        }
    user = await find_existed_user_in_room(sender.id, room.id)
    if user:
        logger.info(f"`{user.id}` can't send a message to this room!")
        results = {
            "status_code": 400,
            "message": "You can't send a message to a room you"
            " have not joined yet.",
        }
    else:
        # create a new message
        results = await send_new_message(sender, request, None, room.id)
    return results
