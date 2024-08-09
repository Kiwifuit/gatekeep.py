from dotenv import load_dotenv
from os import environ
import re
import discord
from discord.ext import commands
from discord import app_commands
from commands import CreateRequest

PATTERN = r"^(09\d{9}|09\d{2} \d{3} \d{4}|639\d{9}|639\d{2} \d{3} \d{4}|\+639\d{9}|\+639\d{2} \d{3} \d{4})$"
GUILD_ID = "1270951090669490207"

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='', intents=intents)

active_users = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await bot.add_cog(CreateRequest(bot))
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

@client.event
async def on_message(message: discord.Message):
    if not isinstance(message.channel, discord.DMChannel) or message.author == client.user:
        return

    if message.author.id not in active_users:
        return

    if not re.match(PATTERN, message.content):
        await message.channel.send("Invalid number. Please provide a valid Philippine phone number.")
        return

    print("Success: Valid phone number received.")
    await message.channel.send("Success: Your number is valid. You can now proceed with your request. To stop the session at any time, type `!stop`." )
    active_users.remove(message.author.id)

    def check(m):
        return m.author == message.author and isinstance(m.channel, discord.DMChannel)

    while True:
        try:
            user_message = await client.wait_for('message', check=check)
            if user_message.content.lower() == '!stop':
                await message.channel.send("Session ended. Thank you!")
                print("Session stopped")
                break
            print(f"USER {message.author.name} sent: {user_message.content}")
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def main():
    load_dotenv()
    client.run(environ["BOT_TOKEN"])

if __name__ == "__main__":
    main()