from dotenv import load_dotenv
from os import environ
import discord

if __name__ == "__main__":
    load_dotenv()

    print(f"Bot Token: {environ["BOT_TOKEN"]!r}")