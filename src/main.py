from dotenv import load_dotenv
from os import environ

import discord
from discord import app_commands

load_dotenv()

BOT_TOKEN = environ["BOT_TOKEN"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@tree.command(
    name="createrequest",
    description="Creates a request",
    guild=discord.Object(id=1270951090669490207)
)
async def first_command(interaction: discord.Interaction):
    user = interaction.user
    try:
        await user.send("Hello User, Please state your request. Ensure your request is both descriptive and concise for a better response.")
        await interaction.response.send_message("I've sent you a DM with further instructions!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't send you a DM. Please check your DM settings.", ephemeral=True)
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1270951090669490207))
    print("Ready!")

client.run(BOT_TOKEN)
