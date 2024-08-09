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
    UnregisteredJob,
)

if __name__ == "__main__":
    load_dotenv()

    conn = connect_db()

    try:
        print("initializing db")
        init_db(conn)
    except DuplicateTable:
        print("db already initialized!")

    users_add(conn, 755257427968000065, "Company", "09229329329")
    workers_add(conn, 755257427968000064, "Misery")
    workers_add(conn, 755257427968000065, "kaiden.")

    workers_set_available(conn, workers_list_available(conn)[1], False)

    print(workers_list_available(conn))

    worker = workers_list_available(conn)[0]
    user = users_get(conn, 755257427968000065)
    available_jobs = [
        UnregisteredJob(user, "Test Homework", "make your mother", 500.0),
        UnregisteredJob(user, "Test Homework #2", "make your father", 5000.0),
        UnregisteredJob(user, "Test Homework #3", "make your sister", 50000.0),
    ]

    for job in available_jobs:
        jobs_add(conn, job)

    available_jobs = jobs_list_available(conn)
    for job_indx in range(2):
        job = available_jobs[job_indx]
        jobs_set_worker(conn, worker, job)

    print(jobs_list_available(conn))
    print(jobs_list_all(conn))
    for job_listed in jobs_list_all(conn):
        print(job_listed)

    job_finished = jobs_get_worker(conn, worker)[1]
    jobs_set_completed(conn, job)

    for job in jobs_get_worker(conn, worker):
        print(job)
