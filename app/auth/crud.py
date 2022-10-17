from fastapi.encoders import jsonable_encoder
import datetime

from app.auth.schemas import UserCreate, UserLoginSchema
from app.users.schemas import UserObjectSchema
from app.utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.crypt_util import get_password_hash, verify_password
from app.utils.jwt_util import create_access_token, timedelta
from app.utils.session import database


async def create_user(user: UserCreate):
    query = """
        INSERT INTO users (
          first_name, last_name, email, password,
          user_status, creation_date
        )
        VALUES
          (
            :first_name, :last_name, :email, :password, 1,
            :creation_date
          )
    """
    values = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
        "creation_date": datetime.datetime.utcnow()
    }
    return await database.execute(query, values=values)


async def find_existed_user(email: str):
    query = "SELECT * FROM users WHERE email=:email AND user_status=1"
    values = {"email": email}
    return await database.fetch_one(query, values=values)


async def find_existed_user_id(id: int):
    query = "SELECT * FROM users WHERE id=:id AND user_status=1"
    values = {"id": id}
    return await database.fetch_one(query, values=values)


async def get_users_with_black_listed_token(token: str):
    query = """
        SELECT
          *
        FROM
          black_listed_tokens
          INNER JOIN access_tokens ON black_listed_tokens.id = access_tokens.id
        where
          access_tokens.token =: token
    """
    values = {"token": token}
    return await database.fetch_one(query, values=values)


async def login_user(form_data):
    user = await find_existed_user(form_data.username)
    if not user:
        return {"status_code": 400, "message": "User not found!"}

    user = UserLoginSchema(email=user.email, password=user.password)
    is_valid = verify_password(form_data.password, user.password)
    if not is_valid:
        return {"status_code": 401, "message": "Invalid Credentials!"}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )
    print(access_token)
    return access_token


async def register_user(user):

    fetched_user = await find_existed_user(user.email)
    if fetched_user:
        return {"status_code": 400, "message": "User already signed up!"}

    # Create new user
    user.password = get_password_hash(user.password)
    await create_user(user)
    user = await find_existed_user(user.email)
    print(user)
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
