import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.auth.crud import find_existed_user
from app.auth.schemas import UserSchema
from app.users import crud as user_crud
from app.users.model import Users
from app.users.schemas import PersonalInfo, UpdateStatus, UserObjectSchema
from app.utils import jwt_util

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
):
    currentUser.first_name = personal_info.first_name
    currentUser.last_name = personal_info.last_name
    currentUser.bio = personal_info.bio
    currentUser.phone_number = personal_info.phone_number
    await currentUser.save()
    return {
        "status_code": 200,
        "message": "Your personal information has been updated successfully!",
    }


@router.get("/user/logout")
async def logout(
    token: str = Depends(jwt_util.get_token_user),
    currentUser: Users = Depends(jwt_util.get_current_active_user),
):
    print(currentUser)
    await user_crud.set_black_list(currentUser.id, token)
    return {"status": 200, "message": "Good Bye!"}


@router.put("/user")
async def update_user_status(
    request: UpdateStatus,
    currentUser=Depends(jwt_util.get_current_active_user),
):
    user = await find_existed_user(email=currentUser.email)
    await user.update(
        chat_status=request.chat_status.lower(),
        modified_date=datetime.datetime.utcnow(),
    )
    return {
        "status_code": 200,
        "message": "Status has been updated successfully!",
    }


@router.get("/users/all/get")
async def get_all_users(currentUser=Depends(jwt_util.get_current_active_user)):
    # Todo
    # return await User.find().all()
    ...
