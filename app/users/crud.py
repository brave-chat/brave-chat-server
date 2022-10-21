import datetime

from app.users.model import (
    Users,
)
from app.utils.session import (
    database,
)


async def deactivate_user(currentUser: Users):
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
    return await database.execute(query, values=values)


async def set_black_list(token: str):
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
    return await database.execute(query, values=values)


async def update_user_info(currentUser: Users):
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
    return await database.execute(query, values=values)


async def update_chat_status(chat_status: str, currentUser: Users):
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
    return await database.execute(query, values=values)
