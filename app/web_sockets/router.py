import asyncio
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.websockets import (
    WebSocket,
)
import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config import (
    settings,
)
from app.utils.pub_sub_handlers import (
    consumer_handler,
    producer_handler,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


@router.websocket("/ws/{sender_id}/{room_name}")
async def websocket_room_endpoint(
    websocket: WebSocket, sender_id: int, room_name: str
):
    try:
        # add user
        # the user on the
        await websocket.accept()
        conn = await settings.redis_conn()
        pubsub = conn.pubsub()

        consumer_task = consumer_handler(
            connection=conn,
            topic=room_name,
            web_socket=websocket,
            sender_id=sender_id,
        )
        producer_task = producer_handler(
            pub_sub=pubsub, topic=room_name, web_socket=websocket
        )
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        logger.debug(f"Done task: {done}")
        for task in pending:
            logger.debug(f"Canceling task: {task}")
            task.cancel()

    except Exception as ex:
        message = f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args!r}"  # noqa: E501
        logger.error(message)
        logger.warning("Disconnecting Websocket")
        await websocket.close()
