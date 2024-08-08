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
    jobs_list_available,
    jobs_list_all,
    jobs_get_worker,
    jobs_set_completed,
    jobs_set_worker,
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

    users_add(cur, 755257427968000065, "09229329329", "Company")
    workers_add(cur, 755257427968000064, "Misery")

    for worker in workers_list_available(cur):
        print(worker)

    worker_uuid, _ = workers_list_available(cur)[0]
    user_uuid, _, _, _ = users_get(cur, 755257427968000065)

    jobs_add(cur, user_uuid, "Test Homework", "make your mother", 500.0)
    jobs_add(cur, user_uuid, "Test Homework #2", "make your father", 5000.0)
    jobs_add(cur, user_uuid, "Test Homework #3", "make your sister", 50000.0)

    for job in jobs_list_available(cur):
        jobs_set_worker(cur, worker_uuid, job[0])

    # print(jobs_list_available(cur))
    # print(jobs_list_all(cur))
    for job_listed in jobs_list_all(cur):
        print(job_listed)
