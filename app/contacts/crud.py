import datetime
import logging

from app.auth.crud import (
    find_existed_user,
)
from app.contacts.model import (
    Contacts,
)
from app.users.model import (
    Users,
)
from app.users.schemas import (
    UserObjectSchema,
)
from app.utils.session import (
    database,
)

logger = logging.getLogger(__name__)


async def create_new_contact(contact_email: str, user_id: int):
    contact = await find_existed_user(email=contact_email)
    if not contact:
        return {
            "status_code": 400,
            "message": "You can't add a non existing user to"
            " your contact list!",
        }
    elif contact.id == user_id:
        return {
            "status_code": 400,
            "message": "You can't add yourself to your contact list!",
        }
    query = """
        SELECT
          *
        FROM
          contacts
        WHERE
          user = :user_id
        AND
          contact = :contact_id
    """
    values = {"user_id": user_id, "contact_id": contact.id}
    found_contact = await database.fetch_one(query, values=values)
    if found_contact:
        return {
            "status_code": 400,
            "message": f"{contact.first_name} already exist in your"
            " contact list!",
        }
    # add contact_id to contact list
    query = """
        INSERT INTO contacts (
          user,
          contact,
          creation_date
        )
        VALUES (
          :user_id,
          :contact_id,
          :creation_date
        )
    """
    values = {
        "user_id": user_id,
        "contact_id": contact.id,
        "creation_date": datetime.datetime.utcnow(),
    }
    await database.execute(query, values=values)
    results = {
        "status_code": 201,
        "message": f"{contact.first_name} has been added to your contact"
        " list!",
    }
    return results


async def get_contacts():
    # get all contacts for each user.
    query = """
        SELECT
          *
        FROM
          contacts
        LEFT JOIN
          users
        ON
          contacts.user= users.id
        GROUP BY
          contacts.id
    """
    contacts = await database.fetch_all(query)
    results = {
        "status_code": 200,
        "result": contacts,
    }
    return results


async def find_existed_user_contact(user_id: int):
    query = "SELECT * FROM contacts WHERE user=:user_id"
    values = {"user_id": user_id}
    return await database.fetch_one(query, values=values)


async def get_user_contacts(user_id: int):
    user = await find_existed_user_contact(user_id)
    if user:
        # get all contacts for each user.
        query = """
            SELECT
              *
            FROM
              contacts
            LEFT JOIN
              users
            ON
              contacts.contact= users.id
            WHERE
              contacts.user= :user_id
        """
        values = {"user_id": user_id}
        contacts = await database.fetch_all(query, values=values)
        results = {"status_code": 200, "result": contacts}
        return results
    return {"status_code": 400, "message": "User not found!"}


async def search_user_contacts(search: str, user_id: int):
    search = search.lower()
    user = await find_existed_user_contact(user_id)
    if user:
        query = """
            SELECT
              *
            FROM
              contacts
            LEFT JOIN
              users
            ON
              contacts.contact= users.id
            WHERE
              contacts.user= :user_id
            AND
              MATCH (
                first_name,
                last_name,
                email
              )
              AGAINST (
                :search
              )
        """
        values = {"user_id": user_id, "search": search}
        return_results = await database.fetch_all(query, values=values)
        results = {"status_code": 200, "result": return_results}
        return results
    return {"status_code": 400, "message": "User not found!"}
