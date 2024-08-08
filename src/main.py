from dotenv import load_dotenv
from os import environ
import re
import discord
from discord import app_commands

PATTERN = r"^(09\d{9}|09\d{2} \d{3} \d{4}|639\d{9}|639\d{2} \d{3} \d{4}|\+639\d{9}|\+639\d{2} \d{3} \d{4})$"
GUILD_ID = "1270951090669490207"

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

active_users = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

@tree.command(
    name="createrequest",
    description="Creates a request",
    guild=discord.Object(id=GUILD_ID)
)
async def create_request(interaction: discord.Interaction):
    user = interaction.user
    user_id = user.id
    active_users[user_id] = True
    try:
        await user.send(f"Hello User `{user_id}`, Please provide your valid `GCash phone number` before proceeding.")
        await interaction.response.send_message("I've sent you a DM with further instructions!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't send you a DM. Please check your DM settings.", ephemeral=True)

@client.event
async def on_message(message: discord.Message):
    if not isinstance(message.channel, discord.DMChannel) or message.author == client.user:
        return

    if message.author.id not in active_users:
        return

    if re.match(PATTERN, message.content):
        print("Success: Valid phone number received.")
        await message.channel.send("Success: Your number is valid. Proceed with your request")
        del active_users[message.author.id]
    else:
        await message.channel.send("Invalid number. Please provide a valid Philippine phone number.")

def main():
    load_dotenv()
    client.run(environ["BOT_TOKEN"])

if __name__ == "__main__":
    main()
