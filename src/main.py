from dotenv import load_dotenv
from os import environ
import re
import discord
from discord.ext import commands


PATTERN = r"^(09\d{9}|09\d{2} \d{3} \d{4}|639\d{9}|639\d{2} \d{3} \d{4}|\+639\d{9}|\+639\d{2} \d{3} \d{4})$"


class Gatekeep(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True

        self.command_cogs = ["commands.user"]

        super().__init__(
            command_prefix="?",
            intents=intents,
            application_id=environ["BOT_APPID"],
        )

    async def setup_hook(self) -> None:
        for command in self.command_cogs:
            await self.load_extension(command)

        await self.tree.sync(guild=discord.Object(id=environ["BOT_GUILD_ID"]))

    async def on_ready(self):
        print("Ready")


if __name__ == "__main__":
    load_dotenv()
    Gatekeep().run(environ["BOT_TOKEN"])
