from aioredis.client import (
    PubSub,
    Redis,
)
from asyncio import (
    ensure_future,
)
import base64
from fastapi.websockets import (
    WebSocket,
)
import json
import logging
import openai
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
    ban_user_from_room,
    find_admin_in_room,
    find_existed_room,
    send_new_room_message,
    unban_user_from_room,
)
from app.users.crud import (
    update_chat_status,
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
        room = None
        admin = None
        if receiver_id:
            data = {
                "content": f"{user.first_name} is online!",
                "type": "online",
                "user": dict(user),
            }
        else:
            room = await find_existed_room(topic, session)
            admin = await find_admin_in_room(sender_id, room.id, session)
            data = {
                "content": f"{user.first_name} is online!",
                "room_name": topic,
                "type": "online",
                "user": dict(user),
            }
        await update_chat_status("online", user, session)
        await connection.publish(topic, json.dumps(data, default=str))
        # wait for messages
        while True:
            if web_socket.application_state == WebSocketState.CONNECTED:
                data = await web_socket.receive_text()
                message_data = json.loads(data)
                message_data["user"] = dict(user)
                if room and not admin:
                    message_data["user"]["admin"] = 1
                if message_data.get("type", None) == "leave":
                    logger.warning(message_data)
                    logger.info("Disconnecting from Websocket")
                    await update_chat_status("offline", user, session)
                    data = {
                        "content": f"{user.first_name} went offline!",
                        "type": "offline",
                        "user": dict(user),
                    }
                    await connection.publish(
                        topic, json.dumps(data, default=str)
                    )
                    await web_socket.close()
                    break
                elif message_data.get("type", None) == "media":
                    data = message_data.pop("content")
                    bin_photo = base64.b64decode(data)
                    # f.write(bin_photo)
                    if receiver_id:
                        receiver = await find_existed_user_id(
                            receiver_id, session
                        )
                        request = RequestContactObject(
                            receiver.email,
                            "",
                            message_data["type"],
                            message_data,
                        )
                        url = await send_new_message(
                            sender_id, request, bin_photo, None, session
                        )
                        message_data["media"] = url
                        message_data["content"] = ""
                        message_data.pop("preview")
                    else:
                        request = RequestRoomObject(
                            topic,
                            "",
                            message_data["type"],
                            message_data,
                        )
                        url = await send_new_room_message(
                            sender_id, request, bin_photo, session
                        )
                        message_data["media"] = url
                        message_data["content"] = ""
                        message_data.pop("preview")
                    await connection.publish(
                        topic, json.dumps(message_data, default=str)
                    )
                    del request
                elif message_data.get("type", None) == "ban":
                    ensure_future(
                        ban_user_from_room(
                            admin_id=sender_id,
                            user_email=message_data["receiver"],
                            room_name=message_data["room_name"],
                            session=session,
                        )
                    )
                    await connection.publish(
                        topic, json.dumps(message_data, default=str)
                    )
                elif message_data.get("type", None) == "unban":
                    ensure_future(
                        unban_user_from_room(
                            admin_id=sender_id,
                            user_email=message_data["receiver"],
                            room_name=message_data["room_name"],
                            session=session,
                        )
                    )
                    await connection.publish(
                        topic, json.dumps(message_data, default=str)
                    )
                elif message_data.get("type", None) == "chatgpt":
                    content = message_data["content"]
                    message_data["user"] = {
                        "id": 100000000000000000,
                        "first_name": "ChatGPT",
                        "last_name": "",
                        "bio": None,
                        "chat_status": "online",
                        "email": "chatgpt@brave-chat.net",
                        "phone_number": None,
                    }
                    message_data["content"] = "start"
                    await connection.publish(
                        topic, json.dumps(message_data, default=str)
                    )
                    message_data["content"] = ""
                    for resp in openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[dict(role="user", content=content)],
                        stream=True,
                    ):
                        resp = resp.choices[0]
                        if "content" not in resp["delta"]:
                            continue
                        if resp["finish_reason"] == "stop":
                            break
                        message_data["content"] += resp["delta"]["content"]
                        print(message_data["content"])
                        await connection.publish(
                            topic, json.dumps(message_data, default=str)
                        )
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
                        ensure_future(
                            send_new_message(
                                sender_id, request, None, None, session
                            )
                        )
                    else:
                        request = RequestRoomObject(
                            topic,
                            message_data["content"],
                            message_data["type"],
                            "",
                        )
                        ensure_future(
                            send_new_room_message(
                                sender_id, request, None, session
                            )
                        )
                    del request
            else:
                logger.warning(
                    f"Websocket state: {web_socket.application_state}."  # noqa: E501
                )
                break
    except Exception as ex:
        message = f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args!r}"  # noqa: E501
        logger.error(message)
        await connection.close()
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
                    f"Websocket state: {web_socket.application_state}."  # noqa: E501
                )
                break
    except Exception as ex:
        message = f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args!r}"  # noqa: E501
        logger.error(message)
        logger.warning("Disconnecting Websocket")
