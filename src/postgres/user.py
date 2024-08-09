from psycopg import Connection
from psycopg.rows import class_row
from .model import User


def users_add(
    db: Connection,
    discord_id: int,
    discord_name: str,
    gcash_number: str,
):
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
        "INSERT INTO users (discord, name, gcash) VALUES (%s, %s, %s)",
        (discord_id, discord_name, gcash_number),
    )


def users_get(db: Connection, discord_id: int) -> User:
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
        "SELECT * FROM users WHERE discord = %s AND registered = true", (discord_id,)
    ).fetchone()
