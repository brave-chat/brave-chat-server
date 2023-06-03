"""Chats router module."""

# conflict between isort and py
# pylint: disable=C0411
from deta import Deta
from fastapi import (
    APIRouter,
    Depends,
    responses,
)
from pydantic import (
    EmailStr,
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
    delete_chat_messages,
    get_chats_user,
    get_sender_receiver_messages,
    send_new_message,
)
from app.chats.schemas import (
    DeleteChatMessages,
    GetAllMessageResults,
    MessageCreate,
)
from app.config import (
    settings,
)
from app.users.schemas import (
    UserObjectSchema,
)
from app.utils.dependencies import (
    get_db_autocommit_session,
)
from app.utils.jwt_util import (
    get_current_active_user,
)

deta = Deta(settings.DETA_PROJECT_KEY)

sent_images = deta.Drive("sent-images")

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
    currentUser: UserObjectSchema = Depends(
        get_current_active_user
    ),  # pylint: disable=C0103
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    The send_message endpoint.
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
    receiver: EmailStr,
    currentUser: UserObjectSchema = Depends(
        get_current_active_user
    ),  # pylint: disable=C0103
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    The get_conversation endpoint.
    """
    results = await get_sender_receiver_messages(
        currentUser, receiver, session
    )
    return results


@router.get(
    "/contacts/chat/search",
    status_code=200,
    name="chats:get-user-chat-list",
)
async def get_chats_user_list(
    search: str,
    currentUser: UserObjectSchema = Depends(
        get_current_active_user
    ),  # pylint: disable=C0103
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    The get_chats_user_list endpoint.
    """
    results = await get_chats_user(currentUser.id, search, session)
    return results


@router.get(
    "/contacts/chat/search/{search}",
    status_code=200,
    name="chats:get-user-chat-list",
)
async def get_chats_user_search_list(
    search: str,
    currentUser: UserObjectSchema = Depends(
        get_current_active_user
    ),  # pylint: disable=C0103
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    The get_chats_user_search_list endpoint.
    """
    results = await get_chats_user(currentUser.id, search, session)
    return results


@router.delete(
    "/user/chat",
    status_code=200,
    name="room:delete-room-chat",
    responses={
        200: {
            "model": ResponseSchema,
            "description": "Return a message that indicates a user"
            " has successfully deleted their messages.",
        },
        400: {
            "model": ResponseSchema,
            "description": "Return a message that indicates if a user"
            " can't delete messages already deleted.",
        },
    },
)
async def delete_user_chat(
    contact: DeleteChatMessages,
    currentUser: UserObjectSchema = Depends(
        get_current_active_user
    ),  # pylint: disable=C0103
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    The delete_user_chat endpoint.
    """
    results = await delete_chat_messages(
        currentUser.id, contact.contact, session
    )
    return results


@router.get("/chat/images/user/{user_id}/{uuid_val}")
async def get_sent_user_chat_images(user_id: int, uuid_val: str):
    """
    The get_sent_user_chat_images endpoint.
    """
    try:
        img = sent_images.get(f"/chat/images/user/{user_id}/{uuid_val}")
        return responses.StreamingResponse(
            img.iter_chunks(), media_type="image/png"
        )
    except Exception:  # pylint: disable=W0703
        return {"status_code": 400, "message": "Something went wrong!"}
