from fastapi import (
    APIRouter,
    Depends,
)
from typing import (
    Union,
)

from app.auth.schemas import (
    ResponseSchema,
)
from app.contacts.crud import (
    create_new_contact,
    get_contacts,
    get_user_contacts,
    search_user_contacts,
)
from app.contacts.model import (
    Contacts,
)
from app.contacts.schemas import (
    AddContact,
    GetAllContactsResults,
)
from app.users.schemas import (
    UserObjectSchema,
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
):
    """
    Add new contact to an authenticated user contacts list.
    """
    results = await create_new_contact(contact.contact, currentUser.id)
    return results


# @router.get(
#     "/contact",
#     status_code=200,
#     response_model=Union[GetAllContactsResults, ResponseSchema],
#     name="contacts:get-all-contacts",
#     responses={
#         200: {
#             "description": "A list of contacts for each user.",
#         },
#     },
# )
# async def get_all_contacts(
#     currentUser: UserObjectSchema = Depends(get_current_active_user),
# ):
#     """
#     Get all contacts grouped by users.
#     """
#     results = await get_contacts()
#     return results


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
):
    """
    Get all contacts for an authenticated user.
    """
    results = await get_user_contacts(currentUser.id)
    return results


@router.get(
    "/contacts/users/search",
    response_model=Union[GetAllContactsResults, ResponseSchema],
    status_code=200,
    name="contacts:search-for-contact",
    responses={
        200: {
            "model": GetAllContactsResults,
            "description": "A list of filtered contacts.",
        },
        400: {
            "model": ResponseSchema,
            "description": "User not found.",
        },
    },
)
async def search_contacts_user(
    search: str,
    currentUser: UserObjectSchema = Depends(get_current_active_user),
):
    """
    Search for a contact given an authenticated user.
    """
    results = await search_user_contacts(search, currentUser.id)
    return results
