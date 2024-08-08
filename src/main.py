from dotenv import load_dotenv
from psycopg.errors import DuplicateTable

from postgres import (
    connect_db,
    init_db,
    users_add,
    users_get,
    workers_add,
    workers_list_available,
    workers_set_available,
    jobs_add,
)

if __name__ == "__main__":
    load_dotenv()
    conn = connect_db()
    cur = conn.cursor()

    try:
        print("initializing db")
        init_db(cur)
    except DuplicateTable:
        print("db already initialized!")

    users_add(cur, 755257427968000065, "09229329329")
    workers_add(cur, 755257427968000064)

    worker_uuid = workers_list_available(cur)[0][0]
    user_uuid, _, _ = users_get(cur, 755257427968000065)

    jobs_add(cur, user_uuid, "Test Homework", "make your mother", 500.0)
    print(worker_uuid, user_uuid)
