from sqlalchemy import (
    exc,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from starlette.requests import (
    Request,
)
from typing import (
    AsyncGenerator,
)


async def get_db_transactional_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = (
        request.app.state.db_transactional_session_factory()
    )

    try:  # noqa: WPS501
        yield session
    except exc.DBAPIError:
        session.rollback()
    finally:
        await session.commit()
        await session.close()


async def get_db_autocommit_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_autocommit_session_factory()

    try:  # noqa: WPS501
        yield session
    except exc.DBAPIError:
        session.rollback()
    finally:
        await session.close()
