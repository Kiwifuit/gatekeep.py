from os import environ
from psycopg import connect, Connection


def connect_db() -> Connection:
    return connect(
        host=environ["PSQL_HOST"],
        database=environ["PSQL_NAME"],
        user=environ["PSQL_USER"],
        password=environ["PSQL_PASS"],
    ).cursor()
