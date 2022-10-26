from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from typing import (
    Union,
)

from app.auth.schemas import (
    ResponseSchema,
)
from app.chats.crud import (
    get_sender_receiver_messages,
    send_new_message,
)
from app.chats.schemas import (
    GetAllMessageResults,
    MessageCreate,
)
from app.users.schemas import (
    UserObjectSchema,
)
from app.utils.dependencies import (
    get_db_autocommit_session,
    get_db_transactional_session,
)
from app.utils.jwt_util import (
    get_current_active_user,
)

router = APIRouter(prefix="/api/v1")


@router.post(
    "/message",
    response_model=ResponseSchema,
    status_code=201,
    name="chats:send-message",
    responses={
        201: {
            "model": ResponseSchema,
            "description": "Message has been delivered successfully!",
        },
        401: {
            "model": ResponseSchema,
            "description": "Empty message, non existing receiver!",
        },
    },
)
async def send_message(
    request: MessageCreate,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    Deliver a new message given an authenticated user.
    """
    results = await send_new_message(
        currentUser.id, request, None, None, session
    )
    return results


@router.get(
    "/conversation",
    response_model=Union[ResponseSchema, GetAllMessageResults],
    status_code=200,
    name="chats:get-all-conversations",
    responses={
        200: {
            "model": GetAllMessageResults,
            "description": "Return a list of messages between two parties.",
        },
    },
)
async def get_conversation(
    receiver: str,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_transactional_session),
):
    """
    Return all messages grouped by senders for a given receiver.
    """
    results = await get_sender_receiver_messages(
        currentUser, receiver, session
    )
    return results
