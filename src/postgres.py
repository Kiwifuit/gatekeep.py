from os import environ
from psycopg import connect, Connection, Cursor


def connect_db() -> Connection:
    """
    Creates a connection to Gatekeep's database

    Returns
    -------
    Connection
        Connection to the database
    """
    return connect(
        host=environ["PSQL_HOST"],
        database=environ["PSQL_NAME"],
        user=environ["PSQL_USER"],
        password=environ["PSQL_PASS"],
    ).cursor()


def init_db(db: Cursor):
    db.execute(
        """
        CREATE TABLE users (
        id UUID DEFAULT gen_random_uuid(),
        discord BIGINT NOT NULL UNIQUE,
        gcash CHAR(11) NOT NULL UNIQUE,

        PRIMARY KEY (id)
        );
        """
    )

    db.execute(
        """
        CREATE TABLE workers (
        id UUID DEFAULT gen_random_uuid(),
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
            REFERENCES users(id)
        CONSTRAINT job_taker
            FOREIGN KEY (wid)
            REFERENCES workers(id)
        );
        """
    )
