from psycopg import Connection
from psycopg.rows import class_row
from .model import (
    Worker,
    Job,
    DisplayableJob,
    UnregisteredJob,
    AvailableJob,
    WorkerJob,
)


def jobs_add(db: Connection, job: UnregisteredJob):
    """
    Adds a job in the database,
    queueing it for work

    Parameters
    ----------
    db : Connection
        Connection to the database
    uid : UUID
        UUID of the user requesting the job
    title : str
        Title of the job
    content : str
        Job context/content
    payment : float
        How much the user is willing to pay for the job
    """
    db.execute(
        "INSERT INTO jobs (uid, title, content, payment) VALUES (%s, %s, %s, %s)",
        (job.user.id, job.title, job.content, job.payment),
    )


def jobs_list_available(db: Connection):
    """
    Lists available jobs ready for taking

    Jobs that are ready are jobs that
    dont have a worker and are not completed

    Parameters
    ----------
    db : Connection
        Connection to the db

    Returns
    -------
    Connection[TupleRow]
        Job Data

    Row Breakdown
    ------------------
    - `int`: Job ID
    - `UUID`: UUID of the job requestor
    - `str`: Title of the job
    - `str`: Additional context the job (job specifics, etc.)
    - `float`: The job's payment on completion
    """
    cur = db.cursor(row_factory=class_row(AvailableJob))
    return cur.execute(
        """
        SELECT jid, users.name as user, title, content, payment
        FROM jobs
        LEFT JOIN users ON jobs.uid = users.id
        WHERE wid IS NULL AND completed = false
        """
    ).fetchall()


def jobs_set_worker(db: Connection, worker: Worker, job: AvailableJob):
    """
    Sets a job as being worked on by a worker

    Parameters
    ----------
    db: Connection
        Connection to the db
    worker_uuid: UUID
        The UUID of the worker assigned
    job_id: int
        The ID of the job being assigned
    """

    db.execute(
        """
        UPDATE jobs
        SET wid = %s
        WHERE jid = %s
        """,
        (worker.id, job.jid),
    )


def jobs_get_worker(db: Connection, worker: Worker):
    """
    Gets the jobs currently assigned to the worker

    Parameters
    ----------
    db : Connection
        Connection to the db
    worker_uuid : UUID
        UUID of the worker to filter

    Returns
    -------
    Connection[TupleRow]
        Job data

    Row Breakdown
    --------------
    `int`: Job ID
    `str`: User's discord name
    `str`: Job title
    `str`: Job specifics
    `float`: How much the user is willing to pay
    """
    cur = db.cursor(row_factory=class_row(WorkerJob))
    return list(
        cur.execute(
            """
        SELECT jid, users.name AS user, title, content, payment
        FROM jobs
        LEFT JOIN users ON jobs.uid = users.id
        WHERE
            wid = %s
            AND
            completed = false
        """,
            (worker.id,),
        )
    )


def jobs_set_completed(db: Connection, job: Job):
    """
    Sets the job as completed

    This function provides no authentication WHATSOEVER
    it is up to the function users to ensure that
    this function runs as intended, however you wish
    to define it.

    Despite intuition, this function does not delete
    data. The only way that job data is deleted is by
    accessing the raw PostgreSQL database and deleting
    data there.

    Parameters
    ----------
    db : Connection
        Connection to the Database
    job_id : int
        Job ID of the job to mark as completed
    """
    db.execute(
        """
        UPDATE jobs
        SET completed = true
        WHERE
          jid = %s
        """,
        (job.jid,),
    )


def jobs_list_all(db: Connection):
    """
    Lists all jobs currently listed in the system

    Since `jobs_set_completed` does not delete data
    whatsoever, this also includes finished jobs

    Parameters
    ----------
    db : Connection
        Connection to the Database

    Returns
    -------
    Connection[TupleRow]
        Job data, including resolved user and worker
        names

    Row Breakdown
    -------------
    `int`: Job ID
    `str`: Worker assigned to job
    `str`: User who requested job
    `str`: Job title
    `str`: Job Specifics
    `bool`: Whether or not the job has been marked as completed
    """
    cur = db.cursor(row_factory=class_row(DisplayableJob))
    return cur.execute(
        """
        SELECT jid, workers.name as worker, users.name as user, title, completed FROM jobs
        LEFT JOIN workers ON jobs.wid = workers.id
        LEFT JOIN users on jobs.uid = users.id
        """
    ).fetchall()
