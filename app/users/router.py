from deta import Deta
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    responses,
)
from fastapi.encoders import (
    jsonable_encoder,
)
import openai
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.auth.schemas import (
    UserSchema,
)
from app.config import (
    settings,
)
from app.users import (
    crud as user_crud,
)
from app.users.models import (
    Users,
)
from app.users.schemas import (
    PersonalInfo,
    ResetPassword,
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

deta = Deta(settings.DETA_PROJECT_KEY)

profile_images = deta.Drive("profile-images")

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
        "message": "Welcome to Brave Chat.",
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


@router.put("/user/reset-password")
async def reset_user_password(
    request: ResetPassword,
    currentUser=Depends(jwt_util.get_current_active_user),
    session: AsyncSession = Depends(get_db_transactional_session),
):
    result = await user_crud.update_user_password(
        request, currentUser, session
    )
    return result


@router.get("/user/profile-image/{name}")
async def get_profile_image(name: str):
    try:
        img = profile_images.get(f"user/{name}/profile.png")
        return responses.StreamingResponse(
            img.iter_chunks(), media_type="image/png"
        )
    except Exception:
        return {"status_code": 400, "message": "Something went wrong!"}


@router.put("/user/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    currentUser: UserObjectSchema = Depends(jwt_util.get_current_active_user),
    session: AsyncSession = Depends(get_db_transactional_session),
):
    try:
        file_name = "user/" + str(currentUser.id) + "/" + "profile.png"
        profile_images.put(file_name, file.file)
        await user_crud.update_profile_picture(
            email=currentUser.email, file_name=file_name, session=session
        )
        return {
            "status_code": 200,
            "message": "Profile picture has been updated!",
        }

    except Exception:
        return {"status_code": 400, "message": "Something went wrong!"}


@router.get("/profile/user/{user_id}/profile.png")
async def get_profile_user_image(user_id: int):
    try:
        img = profile_images.get(f"user/{user_id}/profile.png")
        return responses.StreamingResponse(
            img.iter_chunks(), media_type="image/png"
        )
    except Exception:
        return {"status_code": 400, "message": "Something went wrong!"}


@router.get("/user/openai/key", status_code=200, name="users:openai-key")
def set_openai_api_key(
    apiKey: str,
    _currentUser: UserObjectSchema = Depends(jwt_util.get_current_active_user),
):
    """
    set the openai API key
    """
    openai.api_key = apiKey
