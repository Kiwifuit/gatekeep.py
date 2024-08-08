from dotenv import load_dotenv
from os import environ

if __name__ == "__main__":
    load_dotenv()

    print(f"The bot token is: {environ["BOT_TOKEN"]!r}")
