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

    workers_add(cur, 755257427968000064)
    workers_add(cur, 755257427968000065)
    workers_add(cur, 755257427968000066)
    workers_add(cur, 755257427968000067)

    # Unlist 2nd worker
    workers_set_available(cur, workers_list_available(cur)[1][0], False)

    for worker in workers_list_available(cur):
        print(worker)
