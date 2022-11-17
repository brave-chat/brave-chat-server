import datetime
import logging
from pydantic import (
    EmailStr,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql import (
    text,
)

from app.auth.crud import (
    find_existed_user,
)
from app.chats import (
    crud as chats_crud,
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


async def find_admin_in_room(
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
        AND
          admin = 1
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

    return await session.execute(text(query), values)


async def join_room(
    user_id: int, room_id: int, session: AsyncSession, is_admin=False
):
    if is_admin:
        query = """
            INSERT INTO room_members (
              room,
              member,
              banned,
              admin,
              creation_date
            )
            VALUES (
              :room,
              :member,
              0,
              1,
              :creation_date
            )
        """
    else:
        query = """
            INSERT INTO room_members (
              room,
              member,
              banned,
              admin,
              creation_date
            )
            VALUES (
              :room,
              :member,
              0,
              0,
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
    room_obj.room_name = room_obj.room_name.lower()
    if not room_obj.room_name:
        results = {
            "status_code": 400,
            "message": "Make sure the room name is not empty!",
        }
        return results
    room = await find_existed_room(room_obj.room_name, session)
    if not room:
        if room_obj.join == 0:
            await create_room(
                room_obj.room_name, room_obj.description, session
            )
        else:
            return {
                "status_code": 400,
                "message": "Room not found!",
            }
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
            await join_room(user_id, room.id, session, True)
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
        if user and room_obj.join == 1:
            logger.info(f"`{user_id}` has already joined this room!")
            results = {
                "status_code": 400,
                "message": "You have already joined room "
                f"{room_obj.room_name}!",
            }
        elif not user and room_obj.join == 1:
            await join_room(user_id, room.id, session)
            logger.info(
                f"Adding {user_id} to room `{room_obj.room_name}` as a member."
            )
            results = {
                "status_code": 200,
                "message": f"You have joined room {room_obj.room_name}!",
            }
        else:
            logger.info("This room already exists.")
            results = {
                "status_code": 400,
                "message": "This room already exists. Join it, perhaps?",
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
    sender_id: int,
    request: MessageCreateRoom,
    bin_photo: str,
    session: AsyncSession,
):
    # Check for empty message
    if not request.content and not bin_photo:
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
        logger.info("Can't send a message to this room!")
        results = {
            "status_code": 400,
            "message": "You can't send a message to a room you"
            " have not joined yet.",
        }
    else:
        # create a new message
        if request.media:
            results = await chats_crud.send_new_message(
                sender_id, request, bin_photo, room.id, session
            )
        else:
            results = await chats_crud.send_new_message(
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
            results = await chats_crud.delete_room_messages(
                user_id, room.id, session
            )
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
        return_results = result.fetchall()
        results = {"status_code": 200, "result": return_results}
        return results
    elif user_id and search:
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

    return {"status_code": 400, "message": "Something went wrong!"}


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


async def ban_user_from_room(
    admin_id: int, user_email: EmailStr, room_name: str, session: AsyncSession
):
    room_name = room_name.lower()
    if not room_name:
        return {
            "status_code": 400,
            "message": "Make sure the room name is not empty!",
        }
    room_obj = await find_existed_room(room_name, session)
    if not room_obj:
        return {
            "status_code": 400,
            "message": "Room doesn't exist!",
        }
    admin = await find_admin_in_room(admin_id, room_obj.id, session)
    if not admin:
        return {
            "status_code": 400,
            "message": "You are not the admin of this room!",
        }
    else:
        user_profile = await find_existed_user(user_email, session)
        if not user_profile:
            return {
                "status_code": 400,
                "message": "User not found!",
            }
        room = await find_existed_user_in_room(
            user_profile.id, room_obj.id, session
        )
        if not room:
            results = {
                "status_code": 400,
                "message": f"{user_profile.first_name} is not a member of this room.",
            }
        elif room.member == admin_id:
            results = {
                "status_code": 400,
                "message": "You can't ban yourself!",
            }
        elif room:
            logger.info(
                f"`{admin_id}` has banned" f" from room `{room_name}`!"
            )
            await delete_room_user(room.member, room_obj.id, session)
            results = {
                "status_code": 200,
                "message": f"{user_profile.first_name} has been banned from this room.",
            }
        return results
