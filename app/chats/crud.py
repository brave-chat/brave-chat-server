import datetime
import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql import (
    text,
)

from app.auth.crud import (
    find_existed_user,
)
from app.chats.schemas import (
    MessageCreate,
)
from app.users.schemas import (
    UserObjectSchema,
)

logger = logging.getLogger(__name__)


async def find_existed_user_messages(
    user_id: int,
    session: AsyncSession,
):
    query = """
        SELECT
          *
        FROM
          messages
        WHERE
          sender = :sender_id
        OR
          receiver = :sender_id
    """
    values = {
        "sender_id": user_id,
    }
    result = await session.execute(text(query), values)
    messages = result.fetchall()
    return messages


async def send_new_message(
    sender_id: int,
    request: MessageCreate,
    file,
    room_id: int,
    session: AsyncSession,
):
    # Check for empty message
    if isinstance(request, str) and file:
        # TODO: file upload
        ...
    else:
        if not room_id:
            if not request.content:
                return {
                    "status_code": 400,
                    "message": "You can't send an empty message!",
                }
            receiver = await find_existed_user(
                email=request.receiver, session=session
            )
            if not receiver:
                return {
                    "status_code": 400,
                    "message": "You can't send a message to a non existing"
                    " user!",
                }
            if receiver.id == sender_id:
                return {
                    "status_code": 400,
                    "message": "You can't send a message to yourself!",
                }
            query = """
                INSERT INTO messages (
                  sender,
                  receiver,
                  content,
                  message_type,
                  media,
                  status,
                  creation_date
                )
                VALUES (
                  :sender,
                  :receiver,
                  :content,
                  :message_type,
                  :media,
                  1,
                  :creation_date
                )
            """
            values = {
                "sender": sender_id,
                "receiver": receiver.id,
                "content": request.content,
                "message_type": request.message_type,
                "media": request.media,
                "creation_date": datetime.datetime.utcnow(),
            }
        else:
            query = """
                INSERT INTO messages (
                  sender,
                  room,
                  content,
                  message_type,
                  media,
                  status,
                  creation_date
                )
                VALUES (
                  :sender,
                  :room,
                  :content,
                  :message_type,
                  :media,
                  1,
                  :creation_date
                )
            """
            values = {
                "sender": sender_id,
                "room": room_id,
                "content": request.content,
                "message_type": request.message_type,
                "media": request.media,
                "creation_date": datetime.datetime.utcnow(),
            }
        await session.execute(text(query), values)
    results = {
        "status_code": 201,
        "message": "A new message has been delivered successfully!",
    }
    return results


async def delete_room_messages(
    sender_id: int,
    room_id: int,
    session: AsyncSession,
):

    query = """
        SELECT
            *
        FROM
            messages
        WHERE
          sender = :sender_id
        AND
          room = :room_id
    """
    values = {"sender_id": sender_id, "room_id": room_id}
    result = await session.execute(text(query), values)
    messages = result.fetchall()
    if not messages:
        return {
            "status_code": 400,
            "message": "There is no message to delete!",
        }
    else:
        query = """
            DELETE
            FROM
              messages
            WHERE
              sender = :sender_id
            AND
              room = :room_id
        """
        values = {"sender_id": sender_id, "room_id": room_id}

        await session.execute(text(query), values)

        results = {
            "status_code": 200,
            "message": "Your messages have been deleted successfully!",
        }

    return results


async def get_sender_receiver_messages(
    sender: UserObjectSchema, receiver: str, session: AsyncSession
):
    receiver = await find_existed_user(email=receiver, session=session)
    if not receiver:
        return {
            "status_code": 400,
            "message": "Contact not found!",
        }
    query = """
        SELECT
            id,
            content,
            CASE
                WHEN sender = :sender_id THEN "sent"
                WHEN receiver = :sender_id THEN "received"
                ELSE NULL
            END as type,
            media,
            creation_date
        FROM
            messages
        WHERE (
          sender = :sender_id
            AND
          receiver = :receiver_id
        )
        OR (
          sender = :receiver_id
            AND
          receiver = :sender_id
        )
        ORDER BY
          creation_date
    """
    values = {"sender_id": sender.id, "receiver_id": receiver.id}
    result = await session.execute(text(query), values)
    messages_sent_received = result.fetchall()
    results = {
        "status_code": 200,
        "result": messages_sent_received,
    }
    # Mark received messages by this sender as read
    query = """
        UPDATE
          messages
        SET
          status = 0,
          modified_date = :modified_date
        WHERE
          sender = :receiver_id
        AND
          receiver = :sender_id
    """
    values = {
        "sender_id": sender.id,
        "receiver_id": receiver.id,
        "modified_date": datetime.datetime.utcnow(),
    }
    await session.execute(text(query), values)
    return results


async def get_chats_user(user_id: int, search, session: AsyncSession):
    search = search.lower
    messages = await find_existed_user_messages(user_id, session)
    if messages:
        # get all contacts for each user.
        query = """
            SELECT
              messages.id as id,
              content,
              MAX(messages.creation_date) OVER(PARTITION BY users.email) AS last_message_time,
              SUM(status) OVER(PARTITION BY users.email) AS nb_unread_message,
              users.id as user_id,
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
              messages.receiver = :user_id
        """
        values = {"user_id": user_id}
        result = await session.execute(text(query), values)
        contacts = result.fetchall()
        # HAVING after a window function is not supported by SINGLESTORE
        if contacts:
            contacts = list(
                {
                    dict(myObject)["email"]: dict(myObject)
                    for myObject in contacts
                }.values()
            )
        results = {"status_code": 200, "result": contacts}
        return results
    return {
        "status_code": 200,
        "message": "There are no messages sent to you!",
    }
