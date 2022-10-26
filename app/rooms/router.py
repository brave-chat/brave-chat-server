from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.auth.schemas import (
    ResponseSchema,
)
from app.chats.schemas import (
    MessageCreateRoom,
)
from app.rooms.crud import (
    create_assign_new_room,
    get_room_conversations,
    send_new_room_message,
)
from app.rooms.schemas import (
    RoomCreate,
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
    "/room",
    status_code=200,
    name="room:create-join",
    responses={
        200: {
            "model": ResponseSchema,
            "description": "Return a message that indicates a user has"
            " joined the room.",
        },
        400: {
            "model": ResponseSchema,
            "description": "Return a message that indicates if a user"
            " has already"
            " joined a room ",
        },
    },
)
async def create_room(
    room: RoomCreate,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    Create or join a room.
    """
    results = await create_assign_new_room(currentUser.id, room, session)
    return results


@router.get("/room/conversation", name="room:get-conversations")
async def get_room_users_conversation(
    room: str,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_transactional_session),
):
    """
    Get Room by room name
    """
    results = await get_room_conversations(room, currentUser.id, session)
    return results


@router.post("/room/message", name="room:send-text-message")
async def send_room_message(
    request: MessageCreateRoom,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    Send a new message.
    """
    results = await send_new_room_message(currentUser.id, request, session)
    return results
