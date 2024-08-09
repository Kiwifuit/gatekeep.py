from psycopg import Connection
from psycopg.rows import class_row
from .model import Worker


def workers_add(db: Connection, discord_id: int, discord_name: str):
    """
    Registers a worker to gatekeeper

    Parameters
    ----------
    db : Connection
        Connection to the db
    discord_id : int
        Discord User ID of the to-be worker
    """
    db.execute(
        "INSERT INTO workers (discord, name) VALUES (%s, %s)",
        (discord_id, discord_name),
    )


def workers_set_available(db: Connection, worker: Worker, available: bool):
    """
    Sets a worker's availability to `available`

    By Default, a worker is available when it
    is registered into the database. Doing this
    unlists the user from the list of available workers

    Parameters
    ----------
    db : Connection
        Connection to DB
    id : UUID
        Worker ID
    available : bool
        Worker Availability. `False` to unlist, `True` to relist
    """
    db.execute(
        "UPDATE workers SET able=%s WHERE id=%s AND registered = true",
        (available, worker.id),
    )


def workers_list_available(db: Connection) -> list[Worker]:
    """
    Lists available workers

    Workers whose availability is `False`
    will not show up in this function

    Parameters
    ----------
    db : Connection
        Connection to the db

    Returns
    -------
    Connection[TupleRow]
        List of worker data
    """

    cur = db.cursor(row_factory=class_row(Worker))
    return cur.execute(
        "SELECT id, discord, name FROM workers WHERE able = true AND registered = true"
    ).fetchall()


def workers_delete(db: Connection, worker: Worker):
    """
    Effectively deletes a worker

    For the sake of keeping records, the
    worker data isn't really deleted, but its
    data set to the defaults, and a flag is raised

    Parameters
    ----------
    db : Connection
        Connection to the database
    worker : Worker
        Worker to "delete"
    """
    db.execute(
        """
        UPDATE workers
        SET
          able = false,
          registered = false
        WHERE id = %s
        """,
        (worker.id,),
    )
