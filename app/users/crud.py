from app.users.model import Users
from app.utils.session import database


async def deactivate_user(currentUser: Users):
    query = "UPDATE users SET status=9 WHERE status=1 AND email=:email"
    values = {"email": currentUser.email}
    return await database.execute(query, values=values)


async def set_black_list(token: str):
    # Get token id
    query = "SELECT id FROM access_tokens WHERE token=:token"
    values = {"token": token}
    token_id = await database.fetch_one(query, values=values)
    query = "INSERT INTO black_listed_tokens VALUES (:token)"
    values = {"token": token_id}
    return await database.execute(query, values=values)
