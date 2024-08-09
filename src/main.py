from dotenv import load_dotenv
from psycopg.errors import DuplicateTable
from os import environ

from postgres import (
    connect_db,
    init_db,
    users_add,
    users_get,
    users_delete,
    workers_add,
    workers_delete,
    workers_list_available,
    workers_list_all,
    workers_set_available,
    jobs_add,
    jobs_list_available,
    jobs_list_all,
    jobs_get_worker,
    jobs_set_completed,
    jobs_set_worker,
    UnregisteredJob,
)


def detect_prod():
    if environ.get("PRODUCTION", False):
        print("Gatekeep is running in production")
        return
    print("Detected in development mode. Loading dotenv")
    load_dotenv()


def main():
    detect_prod()

    conn = connect_db()
    print("initializing db")
    init_db(conn)


if __name__ == "__main__":
    main()
