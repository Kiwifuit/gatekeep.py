from dotenv import load_dotenv
from os import environ
import discord

if __name__ == "__main__":
    load_dotenv()

    # burger
    print(f"The bot token is: {environ["BOT_TOKEN"]!r}")