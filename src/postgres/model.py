from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, repr=True)
class User:
    """
    Represents a user that was registered
    in the database

    A user is someone who posts jobs for
    a `Worker` to accept
    """

    id: UUID
    """
    UUID of the user

    This value is generated automatically
    """

    discord: int
    """
    Discord User ID of the user
    """

    name: str
    """
    Discord User Name of the user
    """

    gcash: str
    """
    The user's GCash phone number
    """


@dataclass(frozen=True, repr=True)
class Worker:
    """
    Represents a worker that was registered
    in the database

    A worker is someone who is able to accept
    jobs posted by `User`s
    """

    id: UUID
    """
    UUID of the worker

    This value is generated automatically
    """

    discord: int
    """
    Discord User ID of the worker
    """

    name: str
    """
    Discord User Name of the worker
    """

    available: bool
    """
    Whether or not this user is available

    This value is generated automatically

    """


@dataclass(frozen=True, repr=True)
class Job:
    """
    Represents a job posted by a `User`
    that may or may not have been
    accepted by a `Worker`

    The `uid` and `wid` fields are UUID
    strings. For display-friendly `Job`s
    whose `uid` and `wid` have been
    resolved to names, please refer to
    the `DisplayableJob` dataclass
    """

    jid: int
    """
    Job ID

    This value is generated automatically
    """

    uid: UUID
    """
    The UUID of the `User` who requested
    the job
    """

    wid: UUID
    """
    The UUID of the `Worker` who accepted
    the job.

    This value may be `None` if the job
    has not been accepted
    """

    title: str
    """
    Job Title
    """

    content: str
    """
    Job specifics

    This can include the job's
    - main objective
    - requirements
    - stack
    """

    payment: str
    """
    How much the `User` is willing
    to pay the `Worker` who accepts
    the job
    """

    completed: bool
    """
    Whether or not the job has been completed
    and the finished project has been sent out
    """


@dataclass(frozen=True, repr=True)
class DisplayableJob:
    jid: int
    """
    Job ID

    This value is generated automatically
    """

    worker: str
    """
    Discord username of the worker

    This value may be `None` if the job
    has not been accepted
    """

    user: str
    """
    Discord username of the user who
    requested the job
    """

    title: str
    """
    Job Title
    """

    completed: bool
    """
    Whether or not the job has been completed
    and the finished project has been sent out
    """
