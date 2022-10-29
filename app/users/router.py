from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.encoders import (
    jsonable_encoder,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.auth.schemas import (
    UserSchema,
)
from app.users import (
    crud as user_crud,
)
from app.users.models import (
    Users,
)
from app.users.schemas import (
    PersonalInfo,
    UpdateStatus,
    UserObjectSchema,
)
from app.utils import (
    jwt_util,
)
from app.utils.dependencies import (
    get_db_autocommit_session,
    get_db_transactional_session,
)

router = APIRouter(prefix="/api/v1")


@router.get("/user/profile", response_model=UserSchema)
async def get_user_profile(
    currentUser: UserObjectSchema = Depends(jwt_util.get_current_active_user),
):
    """
    Get user profile info given a token provided in a request header.
    """
    results = {
        "token": None,
        "user": UserObjectSchema(**jsonable_encoder(currentUser)),
        "status_code": 200,
        "message": "Welcome to this blazingly fast chat app.",
    }
    return results


@router.put("/user/profile")
async def update_personal_information(
    personal_info: PersonalInfo,
    currentUser: UserObjectSchema = Depends(jwt_util.get_current_active_user),
    session: AsyncSession = Depends(get_db_transactional_session),
):
    currentUser = UserObjectSchema(**jsonable_encoder(currentUser))
    currentUser.first_name = personal_info.first_name
    currentUser.last_name = personal_info.last_name
    currentUser.bio = personal_info.bio
    currentUser.phone_number = personal_info.phone_number
    await user_crud.update_user_info(currentUser, session)
    return {
        "status_code": 200,
        "message": "Your personal information has been updated successfully!",
    }


@router.get("/user/logout")
async def logout(
    token: str = Depends(jwt_util.get_token_user),
    currentUser: Users = Depends(jwt_util.get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    await user_crud.set_black_list(token, session)
    return {"status": 200, "message": "Good Bye!"}


@router.put("/user")
async def update_user_status(
    request: UpdateStatus,
    currentUser=Depends(jwt_util.get_current_active_user),
    session: AsyncSession = Depends(get_db_transactional_session),
):
    await user_crud.update_chat_status(
        request.chat_status.lower(), currentUser, session
    )
    return {
        "status_code": 200,
        "message": "Status has been updated successfully!",
    }
