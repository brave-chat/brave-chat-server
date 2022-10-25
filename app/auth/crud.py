import datetime
from fastapi.encoders import (
    jsonable_encoder,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql import (
    text,
)

from app.auth.schemas import (
    UserCreate,
    UserLoginSchema,
)
from app.users.schemas import (
    UserObjectSchema,
)
from app.utils.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.utils.crypt_util import (
    get_password_hash,
    verify_password,
)
from app.utils.jwt_util import (
    create_access_token,
    timedelta,
)


async def create_user(user: UserCreate, session: AsyncSession):
    query = """
        INSERT INTO users (
          first_name,
          last_name,
          email,
          password,
          user_status,
          creation_date
        )
        VALUES (
          :first_name,
          :last_name,
          :email,
          :password,
          1,
          :creation_date
        )
    """
    values = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
        "creation_date": datetime.datetime.utcnow(),
    }
    return await session.execute(text(query), values)


async def find_existed_user(email: str, session: AsyncSession):
    query = "SELECT * FROM users WHERE email=:email AND user_status=1"
    values = {"email": email}
    result = await session.execute(text(query), values)
    user = result.fetchone()
    return user


async def find_existed_user_id(id: int, session: AsyncSession):
    query = "SELECT * FROM users WHERE id=:id AND user_status=1"
    values = {"id": id}
    result = await session.execute(text(query), values)
    user = result.fetchone()
    return user


async def get_users_with_black_listed_token(token: str, session: AsyncSession):
    query = """
        SELECT
          *
        FROM
          access_tokens
        WHERE
          token = :token
        AND
          token_status = 0
    """
    values = {"token": token}
    result = await session.execute(text(query), values)
    token = result.fetchone()
    return token


async def login_user(form_data, session: AsyncSession):
    user_obj = await find_existed_user(form_data.username, session)
    if not user_obj:
        return {"status_code": 400, "message": "User not found!"}
    user = UserLoginSchema(email=user_obj.email, password=user_obj.password)
    is_valid = verify_password(form_data.password, user.password)
    if not is_valid:
        return {"status_code": 401, "message": "Invalid Credentials!"}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )
    # save access_token
    query = """
        INSERT INTO
            access_tokens (
                user,
                token,
                creation_date,
                token_status
            )
        VALUES
            (
                :user,
                :token,
                :creation_date,
                1
            )
    """
    values = {
        "user": user_obj.id,
        "token": access_token["access_token"],
        "creation_date": datetime.datetime.utcnow(),
    }
    await session.execute(text(query), values)

    return access_token


async def register_user(user, session: AsyncSession):

    fetched_user = await find_existed_user(user.email, session)
    if fetched_user:
        return {"status_code": 400, "message": "User already signed up!"}

    # Create new user
    user.password = get_password_hash(user.password)
    await create_user(user, session)
    user = await find_existed_user(user.email, session)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    # Serialize user object.
    results = {
        "user": UserObjectSchema(**jsonable_encoder(user)),
        "token": access_token,
        "status_code": 201,
        "message": "You have been registered successfully,"
        "Proceed to the login page...",
    }
    return results
