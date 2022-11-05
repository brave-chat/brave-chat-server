from datetime import (
    datetime,
    timedelta,
)
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
import jwt
from jwt import (
    PyJWTError,
)
from pydantic import (
    ValidationError,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from typing import (
    Dict,
)

from app.auth import (
    crud,
)
from app.auth.schemas import (
    TokenData,
)
from app.users.schemas import (
    UserObjectSchema,
)
from app.utils.constants import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)
from app.utils.dependencies import (
    get_db_transactional_session,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", scheme_name="JWT"
)


def get_token_user(token: str = Depends(oauth2_scheme)) -> str:
    return token


async def create_access_token(
    *, data: Dict[str, str], expires_delta: timedelta = None
) -> Dict[str, str]:
    try:
        payload = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
        payload.update({"exp": expire})
        encoded_jwt_token = jwt.encode(
            payload,
            JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )
        return {"access_token": encoded_jwt_token, "token_type": "bearer"}
    except Exception:
        return {
            "message": "An error has occurred while generating an access"
            " token!"
        }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_transactional_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    black_list = await crud.get_users_with_black_listed_token(token, session)
    if black_list:
        raise credentials_exception
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except (PyJWTError, ValidationError):
        raise credentials_exception
    user = await crud.find_existed_user(token_data.email, session)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: UserObjectSchema = Depends(get_current_user),
):
    if current_user.user_status == 0:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
