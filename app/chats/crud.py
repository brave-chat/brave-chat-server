import datetime
import logging

from app.auth.crud import (
    find_existed_user,
)
from app.chats.model import (
    Messages,
)
from app.chats.schemas import (
    MessageCreate,
)
from app.users.schemas import (
    UserObjectSchema,
)
from app.utils.session import (
    database,
)

logger = logging.getLogger(__name__)


async def send_new_message(
    sender: UserObjectSchema, request: MessageCreate, file
):
    # Check for empty message
    if isinstance(request, str) and file:
        # TODO: file upload
        ...
    else:
        if not request.content:
            return {
                "status_code": 400,
                "message": "You can't send an empty message!",
            }
        receiver = await find_existed_user(email=request.receiver)
        if not receiver:
            return {
                "status_code": 400,
                "message": "You can't send a message to a non existing user!",
            }
        if receiver.id == sender.id:
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
              creation_date
            )
            VALUES (
              :sender,
              :receiver,
              :content,
              :message_type,
              :media,
              :creation_date
            )
        """
        values = {
            "sender": sender.id,
            "receiver": receiver.id,
            "content": request.content,
            "message_type": request.message_type,
            "media": "",
            "creation_date": datetime.datetime.utcnow(),
        }
        await database.execute(query, values=values)
    results = {
        "status_code": 201,
        "message": "A new message has been delivered successfully!",
    }
    return results


async def get_sender_receiver_messages(
    sender: UserObjectSchema, receiver: str
):
    receiver = await find_existed_user(email=receiver)
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
    messages_sent_received = await database.fetch_all(query, values=values)
    results = {
        "status_code": 200,
        "result": messages_sent_received,
    }
    return results
