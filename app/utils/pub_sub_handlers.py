from aioredis.client import (
    PubSub,
    Redis,
)
from fastapi.websockets import (
    WebSocket,
    WebSocketDisconnect,
)
import json
import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from starlette.websockets import (
    WebSocketState,
)
from typing import (
    NamedTuple,
    Optional,
)

from app.auth.crud import (
    find_existed_user_id,
)
from app.chats.crud import (
    send_new_message,
)
from app.rooms.crud import (
    send_new_room_message,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestRoomObject(NamedTuple):
    room: str
    content: str
    message_type: str
    media: str


class RequestContactObject(NamedTuple):
    receiver: str
    content: str
    message_type: str
    media: str


async def consumer_handler(
    connection: Redis,
    topic: str,
    web_socket: WebSocket,
    sender_id: int,
    receiver_id: Optional[int],
    session: AsyncSession,
) -> None:
    try:
        user = await find_existed_user_id(sender_id, session)
        if receiver_id:
            data = {
                "content": f"{user.first_name} is online!",
                "type": "online",
                "user": dict(user),
            }
        else:
            data = {
                "content": f"{user.first_name} has joined the room!",
                "room_name": topic,
                "type": "entrance",
                "user": dict(user),
            }
        await connection.publish(topic, json.dumps(data, default=str))
        # wait for messages
        while True:
            if web_socket.application_state == WebSocketState.CONNECTED:
                data = await web_socket.receive_text()
                message_data = json.loads(data)
                message_data["user"] = dict(user)
                if message_data.get("type", None) == "leave":
                    logger.warning(message_data)
                    logger.info("Disconnecting from Websocket")
                    # await web_socket.close()
                    # break
                else:
                    logger.info(
                        f"CONSUMER RECIEVED: {json.dumps(message_data, default=str)}"  # noqa: E501
                    )
                    await connection.publish(
                        topic, json.dumps(message_data, default=str)
                    )
                    if receiver_id:
                        receiver = await find_existed_user_id(
                            receiver_id, session
                        )
                        request = RequestContactObject(
                            receiver.email,
                            message_data["content"],
                            message_data["type"],
                            "",
                        )
                        await send_new_message(
                            sender_id, request, None, None, session
                        )
                    else:
                        request = RequestRoomObject(
                            topic,
                            message_data["content"],
                            message_data["type"],
                            "",
                        )
                        await send_new_room_message(
                            sender_id, request, session
                        )
                    del request
            else:
                logger.warning(
                    f"Websocket state: {web_socket.application_state}, reconnecting..."  # noqa: E501
                )
                await web_socket.accept()
    except Exception as ex:
        message = f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args!r}"  # noqa: E501
        logger.error(message)
        # remove user
        logger.warning("Disconnecting Websocket")


async def producer_handler(
    pub_sub: PubSub, topic: str, web_socket: WebSocket
) -> None:
    await pub_sub.subscribe(topic)
    try:
        while True:
            if web_socket.application_state == WebSocketState.CONNECTED:
                message = await pub_sub.get_message(
                    ignore_subscribe_messages=True
                )
                if message:
                    logger.info(
                        f"PRODUCER SENDING: {json.dumps(message, default=str)}"
                    )
                    await web_socket.send_text(
                        json.dumps(message["data"], default=str)
                    )
            else:
                logger.warning(
                    f"Websocket state: {web_socket.application_state}, reconnecting..."  # noqa: E501
                )
                # await web_socket.accept()
    except Exception as ex:
        message = f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args!r}"  # noqa: E501
        logger.error(message)
        logger.warning("Disconnecting Websocket")
