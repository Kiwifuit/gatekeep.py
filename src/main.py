from dotenv import load_dotenv
from os import environ
import discord

if __name__ == "__main__":
    load_dotenv()

    print(environ["BOT_TOKEN"])