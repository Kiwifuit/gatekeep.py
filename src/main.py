from dotenv import load_dotenv
from os import environ

from postgres import connect_db, init_db

DATABASE = connect_db()

if __name__ == "__main__":
    load_dotenv()
    init_db(DATABASE.cursor())

    print(f"The bot token is: {environ["BOT_TOKEN"]!r}")
