from psycopg import connect, Connection, Cursor
from os import environ
from .user import users_add, users_get
from .worker import workers_add, workers_list_available, workers_set_available
from .job import (
    jobs_add,
    jobs_get_worker,
    jobs_list_all,
    jobs_list_available,
    jobs_set_completed,
    jobs_set_completed,
    jobs_set_worker,
)
from .model import UnregisteredJob


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


def init_db(db: Connection):
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
        name VARCHAR(32) NOT NULL,
        gcash CHAR(11) NOT NULL UNIQUE,
        registered BOOLEAN DEFAULT true,

        PRIMARY KEY (id)
        );
        """
    )

    db.execute(
        """
        CREATE TABLE workers (
        id UUID DEFAULT gen_random_uuid() UNIQUE,
        discord BIGINT NOT NULL UNIQUE,
        name VARCHAR(32) NOT NULL,
        able BOOLEAN DEFAULT true,
        registered BOOLEAN DEFAULT true,

        PRIMARY KEY (id)
        );
        """
    )

    db.execute(
        """
        CREATE TABLE jobs (
        uid UUID NOT NULL,
        wid UUID,
        jid SMALLSERIAL NOT NULL UNIQUE,
        title VARCHAR(64) NOT NULL,
        content TEXT NOT NULL,
        payment REAL NOT NULL,
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
