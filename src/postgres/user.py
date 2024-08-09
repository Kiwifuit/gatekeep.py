from psycopg import Connection
from psycopg.rows import class_row
from model import User


def users_add(db: Connection, discord_id: int, gcash_number: str, discord_name: str):
    """
    Adds a user

    Parameters
    ----------
    db : Connection
        Connection to the db
    discord_id : int
        Discord User's ID
    gcash_number : str
        GCash Number, provided by user
    """
    db.execute(
        "INSERT INTO users (user_discord, gcash, user_name) VALUES (%s, %s, %s)",
        (discord_id, gcash_number, discord_name),
    )


def users_get(db: Connection, discord_id: int) -> list[User]:
    """
    Gets a user from the db

    Parameters
    ----------
    db : Connection
        Connection to the db
    discord_id : int
        ID of the discord user who sent the message

    Returns
    -------
    Connection[TupleRow]
        Discord User's information
        `UUID`: User ID
        `int`: User Discord ID
        `str`: User GCash Number
    """
    conn = db.cursor(row_factory=class_row(User))

    return conn.execute(
        "SELECT * FROM users WHERE user_discord = %s", (discord_id,)
    ).fetchone()
