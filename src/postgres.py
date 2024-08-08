from os import environ
from uuid import UUID

from psycopg import connect, Connection, Cursor


def connect_db() -> Connection:
    """
    Creates a connection to Gatekeep's database

    Returns
    -------
    Connection
        Connection to the database
    """
    # print(environ["PSQL_URL"])
    return connect(environ["PSQL_URL"])


def init_db(db: Cursor):
    """
    Initializes Gatekeep's Database

    This function should only raise an
    `psycopg.errors.DuplicateTable` error

    Parameters
    ----------
    db : Cursor
        cursor initialized by `connect_db`
    """
    db.execute(
        """
        CREATE TABLE users (
        id UUID DEFAULT gen_random_uuid() UNIQUE,
        discord BIGINT NOT NULL UNIQUE,
        gcash CHAR(11) NOT NULL UNIQUE,

        PRIMARY KEY (id)
        );
        """
    )

    db.execute(
        """
        CREATE TABLE workers (
        id UUID DEFAULT gen_random_uuid() UNIQUE,
        discord BIGINT NOT NULL UNIQUE,
        able BOOLEAN DEFAULT true
        );
        """
    )

    db.execute(
        """
        CREATE TABLE jobs (
        uid UUID NOT NULL,
        wid UUID,
        jid SMALLSERIAL NOT NULL,
        title VARCHAR(64) NOT NULL,
        content TEXT NOT NULL,
        payment MONEY NOT NULL,
        completed BOOLEAN DEFAULT false,

        PRIMARY KEY(jid),
        CONSTRAINT job_owner
            FOREIGN KEY (uid)
            REFERENCES users(id),
        CONSTRAINT job_taker
            FOREIGN KEY (wid)
            REFERENCES workers(id)
        );
        """
    )


def users_add(db: Cursor, discord_id: int, gcash_number: str):
    """
    Adds a user

    Parameters
    ----------
    db : Cursor
        Cursor to the db
    discord_id : int
        Discord User's ID
    gcash_number : str
        GCash Number, provided by user
    """
    db.execute(
        "INSERT INTO users (discord, gcash) VALUES (%s, %s)", (discord_id, gcash_number)
    )


def users_get(db: Cursor, discord_id: int) -> tuple[UUID, int, str]:
    """
    Gets a user from the db

    Parameters
    ----------
    db : Cursor
        Cursor to the db
    discord_id : int
        ID of the discord user who sent the message

    Returns
    -------
    tuple[UUID, int, str]
        Discord User's information
        `UUID`: User ID
        `int`: User Discord ID
        `str`: User GCash Number
    """
    return db.execute(
        "SELECT * FROM users WHERE discord = %s", (discord_id,)
    ).fetchone()


def workers_add(db: Cursor, discord_id: int):
    """
    Registers a worker to gatekeeper

    Parameters
    ----------
    db : Cursor
        Cursor to the db
    discord_id : int
        Discord User ID of the to-be worker
    """
    db.execute("INSERT INTO workers (discord) VALUES (%s)", (discord_id,))


def workers_set_available(db: Cursor, id: UUID, available: bool):
    """
    Sets a worker's availability to `available`

    By Default, a worker is available when it
    is registered into the database. Doing this
    unlists the user from the list of available workers

    Parameters
    ----------
    db : Cursor
        Cursor to DB
    id : UUID
        Worker ID
    available : bool
        Worker Availability. `False` to unlist, `True` to relist
    """
    db.execute("UPDATE workers SET able=%s WHERE id=%s", (available, id))


def workers_list_available(db: Cursor) -> list[tuple[UUID, str]]:
    """
    Lists available workers

    Workers whose availability is `False`
    will not show up in this function

    Parameters
    ----------
    db : Cursor
        Cursor to the db

    Returns
    -------
    list[tuple[UUID, str]]
        List of worker data
    """

    return list(
        map(
            lambda r: r[0],
            db.execute(
                "SELECT (id, discord) FROM workers WHERE able = true"
            ).fetchall(),
        )
    )
