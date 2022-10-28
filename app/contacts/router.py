from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from typing import (
    Union,
)

from app.auth.schemas import (
    ResponseSchema,
)
from app.contacts.crud import (
    create_new_contact,
    delete_contact_user,
    get_contacts,
    get_user_contacts,
    search_user_contacts,
)
from app.contacts.schemas import (
    AddContact,
    GetAllContactsResults,
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
    "/contact",
    response_model=ResponseSchema,
    status_code=201,
    name="contacts:add-contact",
    responses={
        201: {
            "model": ResponseSchema,
            "description": "Return a message that indicates a new user"
            "has been added to a contact list.",
        },
        400: {
            "model": ResponseSchema,
            "description": "Return this response in case of non existing user"
            " or an already existed one in the contact list.",
        },
    },
)
async def add_contact(
    contact: AddContact,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    Add new contact to an authenticated user contacts list.
    """
    results = await create_new_contact(
        contact.contact, currentUser.id, session
    )
    return results


@router.get(
    "/contacts",
    response_model=Union[GetAllContactsResults, ResponseSchema],
    status_code=200,
    name="contacts:get-all-user-contacts",
    responses={
        200: {
            "model": GetAllContactsResults,
            "description": "A list of contacts for each user.",
        },
        400: {
            "model": ResponseSchema,
            "description": "User not found.",
        },
    },
)
async def get_contacts_user(
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    Get all contacts for an authenticated user.
    """
    results = await get_user_contacts(currentUser.id, session)
    return results


@router.get(
    "/contacts/users/search",
    status_code=200,
    name="contacts:search-for-contact",
    responses={
        200: {
            "model": GetAllContactsResults,
            "description": "A list of filtered contacts.",
        },
        400: {
            "model": ResponseSchema,
            "description": "User can't search against an empty string, or"
            " User not found.",
        },
    },
)
async def search_contacts_user(
    search: str,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    Search for a contact given an authenticated user.
    """
    results = await search_user_contacts(search, currentUser.id, session)
    return results


@router.delete(
    "/contact/delete",
    status_code=200,
    name="contacts:delete-contact",
    responses={
        200: {
            "model": ResponseSchema,
            "description": "Return a message that indicates a user"
            " has deleted a contact.",
        },
        400: {
            "model": ResponseSchema,
            "description": "Return a message that indicates if a user"
            " can't delete a non existing contact.",
        },
    },
)
async def delete_user_contact(
    contact: AddContact,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_autocommit_session),
):
    """
    delete a contact.
    """
    results = await delete_contact_user(
        contact.contact, currentUser.id, session
    )
    return results
