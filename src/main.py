from dotenv import load_dotenv
from os import environ
from psycopg.errors import DuplicateTable

from postgres import connect_db, init_db

if __name__ == "__main__":
    load_dotenv()
    database = connect_db()

    try:
        print("initializing db")
        init_db(database.cursor())
    except DuplicateTable:
        print("db already initialized!")

    print(f"The bot token is: {environ["BOT_TOKEN"]!r}")
