import datetime
import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql import (
    text,
)

from app.chats.crud import (
    delete_room_messages,
    send_new_message,
)
from app.chats.schemas import (
    MessageCreateRoom,
)

logger = logging.getLogger(__name__)


async def find_existed_room(room_name: str, session: AsyncSession):
    query = """
        SELECT
          *
        FROM
          rooms
        WHERE
          room_name = :room_name
    """
    values = {"room_name": room_name}

    result = await session.execute(text(query), values)
    return result.fetchone()


async def find_existed_user_in_room(
    user_id: int, room_id: int, session: AsyncSession
):
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

    result = await session.execute(text(query), values)
    return result.fetchone()


async def create_room(room_name: int, description: str, session: AsyncSession):
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

    result = await session.execute(text(query), values)
    return result.fetchone()


async def join_room(user_id: int, room_id: int, session: AsyncSession):
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

    return await session.execute(text(query), values)


async def delete_room_user(user_id: int, room_id: int, session: AsyncSession):
    query = """
        DELETE
        FROM
          room_members
        WHERE
          room = :room
        AND
          member = :member
    """
    values = {"room": room_id, "member": user_id}

    return await session.execute(text(query), values)


async def create_assign_new_room(
    user_id: int, room_obj, session: AsyncSession
):
    if not room_obj.room_name:
        results = {
            "status_code": 400,
            "message": "Make sure the room name is not empty!",
        }
        return results
    room = await find_existed_room(room_obj.room_name, session)
    if not room:
        await create_room(room_obj.room_name, room_obj.description, session)
        logger.info(f"Creating room `{room_obj.room_name}`.")
        room = await find_existed_room(room_obj.room_name, session)
        user = await find_existed_user_in_room(user_id, room.id, session)
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
        user = await find_existed_user_in_room(user_id, room.id, session)
        if user:
            logger.info(f"`{user_id}` has already joined this room!")
            results = {
                "status_code": 400,
                "message": "You have already joined room "
                f"{room_obj.room_name}!",
            }
        else:
            await join_room(user_id, room.id, session)
            logger.info(
                f"Adding {user_id} to room `{room_obj.room_name}` as a member."
            )
            results = {
                "status_code": 200,
                "message": f"You have joined room {room_obj.room_name}!",
            }
        return results


async def get_room_conversations(
    room_name: str, sender_id: int, session: AsyncSession
):
    room = await find_existed_room(room_name, session)
    if not room:
        return {
            "status_code": 400,
            "message": "Room not found!",
        }
    query = """
        SELECT
            messages.id as msg_id,
            messages.content,
            CASE
                WHEN messages.sender = :sender_id THEN "sent"
                ELSE "received"
            END as type,
            messages.media,
            messages.creation_date,
            users.id as id,
            users.first_name,
            users.last_name,
            users.bio,
            users.chat_status,
            users.email,
            users.phone_number,
            users.profile_picture

        FROM
            messages
        LEFT JOIN
            users
        ON
          messages.sender = users.id
        WHERE
          messages.room = :room_id
        ORDER BY
          messages.creation_date
    """
    values = {"room_id": room.id, "sender_id": sender_id}
    result = await session.execute(text(query), values)
    messages_sent_received = result.fetchall()
    results = {
        "status_code": 200,
        "result": messages_sent_received,
    }
    return results


async def send_new_room_message(
    sender_id: int, request: MessageCreateRoom, session: AsyncSession
):
    # Check for empty message
    if not request.content:
        return {
            "status_code": 400,
            "message": "You can't send an empty message!",
        }
    room = await find_existed_room(request.room, session)
    if not room:
        return {
            "status_code": 400,
            "message": "You can't send a message to a non existing room!",
        }
    user = await find_existed_user_in_room(sender_id, room.id, session)
    if not user:
        logger.info(f"`{user.id}` can't send a message to this room!")
        results = {
            "status_code": 400,
            "message": "You can't send a message to a room you"
            " have not joined yet.",
        }
    else:
        # create a new message
        results = await send_new_message(
            sender_id, request, None, room.id, session
        )
    return results


async def leave_room_user(user_id: int, room_name, session: AsyncSession):
    if not room_name:
        results = {
            "status_code": 400,
            "message": "Make sure the room name is not empty!",
        }
        return results
    room = await find_existed_room(room_name, session)
    if not room:
        logger.info("Can't leave a non existing room!")
        results = {
            "status_code": 400,
            "message": "You can't leave a non existing room",
        }
    else:
        user = await find_existed_user_in_room(user_id, room.id, session)
        if user:
            await delete_room_user(user_id, room.id, session)
            logger.info(f"`{user_id}` has left this room!")
            results = {
                "status_code": 200,
                "message": f"You have left room {room_name}!",
            }
        else:
            logger.info(
                f"User {user_id} is not a member of room `{room_name}`."
            )
            results = {
                "status_code": 200,
                "message": f"You are not a member of room {room_name}!",
            }
    return results


async def delete_room_user_chat(
    user_id: int, room_name, session: AsyncSession
):
    if not room_name:
        results = {
            "status_code": 400,
            "message": "Make sure the room name is not empty!",
        }
        return results
    room = await find_existed_room(room_name, session)
    if not room:
        logger.info("Can't delete messages in a non existing room!")
        results = {
            "status_code": 400,
            "message": "You can't delete messages in a non existing room!",
        }
    else:
        user = await find_existed_user_in_room(user_id, room.id, session)
        if user:
            results = await delete_room_messages(user_id, room.id, session)
            logger.info(
                f"`{user_id}` has deleted their messages in this room!"
            )
        else:
            logger.info(
                f"User {user_id} is not a member of room `{room_name}`."
            )
            results = {
                "status_code": 200,
                "message": f"You are not a member of room {room_name}!",
            }
    return results


async def search_rooms(search: str, user_id: int, session: AsyncSession):
    if not search:
        results = {
            "status_code": 400,
            "result": "You can't search against an empty string!",
        }
        return results
    query = """
        SELECT
          *
        FROM
          room_members
        LEFT JOIN
          rooms
        ON
          room_members.room= rooms.id
        WHERE
          room_members.member= :user_id
        AND
          INSTR(room_name, :search) > 0
    """
    values = {"user_id": user_id, "search": search.lower()}
    result = await session.execute(text(query), values)
    return_results = result.fetchall()
    results = {"status_code": 200, "result": return_results}
    return results


async def get_rooms_user(user_id: int, session: AsyncSession):
    # get all rooms for this user.
    query = """
        SELECT
          *
        FROM
          room_members
        LEFT JOIN
          rooms
        ON
          room_members.room= rooms.id
        WHERE
          room_members.member= :user_id
    """
    values = {"user_id": user_id}

    result = await session.execute(text(query), values)
    contacts = result.fetchall()
    results = {"status_code": 200, "result": contacts}
    return results
