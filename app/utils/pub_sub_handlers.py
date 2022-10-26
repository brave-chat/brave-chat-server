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

from app.auth.crud import (
    find_existed_user_id,
)
from app.rooms.crud import (
    send_new_room_message,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consumer_handler(
    connection: Redis,
    topic: str,
    web_socket: WebSocket,
    sender_id: int,
) -> None:
    try:
        data = {
            "content": f"{sender_id} has joined the room!",
            "room_name": topic,
            "type": "entrance",
            "user": sender_id,
        }
        await connection.publish(topic, json.dumps(data, default=str))
        # wait for messages
        while True:
            if web_socket.application_state == WebSocketState.CONNECTED:
                data = await web_socket.receive_text()
                message_data = json.loads(data)
                message_data["user"] = sender_id
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
                    # TODO: Build a request object
                    # send_new_room_message(sender_id, request, session)
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
                await web_socket.accept()
    except Exception as ex:
        message = f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args!r}"  # noqa: E501
        logger.error(message)
        logger.warning("Disconnecting Websocket")
