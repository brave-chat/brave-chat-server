import datetime
import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql import (
    text,
)

from app.auth.crud import (
    find_existed_user,
)

logger = logging.getLogger(__name__)


async def create_new_contact(
    contact_email: str, user_id: int, session: AsyncSession
):
    contact = await find_existed_user(email=contact_email, session=session)
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
    result = await session.execute(text(query), values)
    found_contact = result.fetchone()
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

    await session.execute(text(query), values)
    results = {
        "status_code": 201,
        "message": f"{contact.first_name} has been added to your contact"
        " list!",
    }
    return results


async def delete_contact_user(
    contact_email: str, user_id: int, session: AsyncSession
):
    contact = await find_existed_user(email=contact_email, session=session)
    if not contact:
        return {
            "status_code": 400,
            "message": "You can't delete a non existing user!",
        }
    elif contact.id == user_id:
        return {
            "status_code": 400,
            "message": "You can't delete yourself!",
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
    result = await session.execute(text(query), values)
    contacts = result.fetchall()
    if not contacts:
        return {
            "status_code": 400,
            "message": "There is no contact to delete!",
        }
    else:
        query = """
            DELETE
            FROM
              contacts
            WHERE
              user = :user_id
            AND
              contact = :contact_id
        """
        values = {"user_id": user_id, "contact_id": contact.id}
        await session.execute(text(query), values)

        results = {
            "status_code": 200,
            "message": f"{contact.first_name} has been deleted from your"
            " contact list!",
        }
    return results


async def get_contacts(session: AsyncSession):
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
    values = {}
    result = await session.execute(text(query), values)
    contacts = result.fetchall()
    results = {
        "status_code": 200,
        "result": contacts,
    }
    return results


async def find_existed_user_contact(user_id: int, session: AsyncSession):
    query = "SELECT * FROM contacts WHERE user=:user_id"
    values = {"user_id": user_id}
    result = await session.execute(text(query), values)
    return result.fetchone()


async def get_user_contacts(user_id: int, session: AsyncSession):
    user = await find_existed_user_contact(user_id, session)
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

        result = await session.execute(text(query), values)
        contacts = result.fetchall()
        results = {"status_code": 200, "result": contacts}
        return results
    return {"status_code": 400, "message": "User not found!"}


async def search_user_contacts(
    search: str, user_id: int, session: AsyncSession
):
    user = await find_existed_user_contact(user_id, session)
    if not search or len(search) == 0:
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
        result = await session.execute(text(query), values)
        return_results = result.fetchall()
        results = {"status_code": 200, "result": return_results}
        return results

    elif user and search:
        # TODO: CONCAT(*, :search, *)
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
        result = await session.execute(text(query), values)
        return_results = result.fetchall()
        results = {"status_code": 200, "result": return_results}
        return results

    return {"status_code": 400, "message": "User not found!"}
