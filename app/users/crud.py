import datetime
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql import (
    text,
)

from app.auth.crud import (
    find_existed_user,
)
from app.users.models import (
    Users,
)
from app.users.schemas import (
    ResetPassword,
)
from app.utils.crypt_util import (
    get_password_hash,
    verify_password,
)


async def deactivate_user(currentUser: Users, session: AsyncSession):
    query = """
        UPDATE
          users
        SET
          user_status = 0,
          modified_date = :modified_date
        WHERE
          user_status = 1
          AND email = :email
    """
    values = {
        "email": currentUser.email,
        "modified_date": datetime.datetime.utcnow(),
    }

    return await session.execute(text(query), values)


async def set_black_list(token: str, session: AsyncSession):
    query = """
        UPDATE
          access_tokens
        SET
          token_status = 0,
          modified_date = :modified_date
        WHERE
          token_status = 1
          AND token = :token
    """
    values = {
        "token": token,
        "modified_date": datetime.datetime.utcnow(),
    }

    return await session.execute(text(query), values)


async def update_user_info(currentUser: Users, session: AsyncSession):
    query = """
        UPDATE
          users
        SET
          first_name = :first_name,
          last_name = :last_name,
          bio = :bio,
          phone_number = :phone_number,
          modified_date = :modified_date
        WHERE
          user_status = 1
          AND email = :email
    """
    values = {
        "first_name": currentUser.first_name,
        "last_name": currentUser.last_name,
        "bio": currentUser.bio,
        "phone_number": currentUser.phone_number,
        "email": currentUser.email,
        "modified_date": datetime.datetime.utcnow(),
    }

    return await session.execute(text(query), values)


async def update_chat_status(
    chat_status: str, currentUser: Users, session: AsyncSession
):
    query = """
        UPDATE
          users
        SET
          chat_status = :chat_status,
          modified_date = :modified_date
        WHERE
          user_status = 1
          AND email = :email
    """
    values = {
        "chat_status": chat_status,
        "email": currentUser.email,
        "modified_date": datetime.datetime.utcnow(),
    }

    return await session.execute(text(query), values)


async def update_user_password(
    request: ResetPassword, currentUser: Users, session: AsyncSession
):
    user = await find_existed_user(currentUser.email, session)
    if not verify_password(request.old_password, user.password):
        results = {
            "status_code": 400,
            "message": "Your old password is not correct!",
        }
    elif verify_password(request.new_password, user.password):
        results = {
            "status_code": 400,
            "message": "Your new password can't be your old one!",
        }
    elif not request.new_password == request.confirm_password:
        results = {
            "status_code": 400,
            "message": "Please confirm your new password!",
        }
    else:
        query = """
            UPDATE
              users
            SET
              password = :password,
              modified_date = :modified_date
            WHERE
              user_status = 1
              AND email = :email
        """
        values = {
            "password": get_password_hash(request.new_password),
            "email": currentUser.email,
            "modified_date": datetime.datetime.utcnow(),
        }
        await session.execute(text(query), values)
        results = {
            "status_code": 200,
            "message": "Your password has been reseted successfully!",
        }
        await session.execute(text(query), values)
    return results


async def update_profile_picture(
    email: str, file_name: str, session: AsyncSession
):
    query = """
        UPDATE
          users
        SET
          profile_picture = :file_name,
          modified_date = :modified_date
        WHERE
          user_status = 1
          AND email = :email
    """
    values = {
        "file_name": file_name,
        "email": email,
        "modified_date": datetime.datetime.utcnow(),
    }

    return await session.execute(text(query), values)
