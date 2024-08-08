from dotenv import load_dotenv
from os import environ
from psycopg.errors import DuplicateTable

from postgres import connect_db, init_db, users_add, users_get

if __name__ == "__main__":
    load_dotenv()
    conn = connect_db()
    cur = conn.cursor()

    try:
        print("initializing db")
        init_db(cur)
    except DuplicateTable:
        print("db already initialized!")

    # print(f"The bot token is: {environ["BOT_TOKEN"]!r}")
    users_add(cur, 755257427968000065, "09224140700")
    user = users_get(cur, 755257427968000065)

    print(user)
