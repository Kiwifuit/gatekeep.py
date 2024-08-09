import discord
from discord.ext import commands
from discord import app_commands

GUILD_ID = "1270951090669490207"

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

active_users = []

class CreateRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tree.command(
        name="createrequest",
        description="Creates a request",
        guild=discord.Object(id=GUILD_ID)
    )
    async def create_request(self, interaction: discord.Interaction):
        user = interaction.user
        user_id = user.id
        username = user.name

        if user_id in active_users:
            await interaction.response.send_message("You already have a pending request. Please finish it before creating another request.", ephemeral=True)
            return

        active_users.append(user_id)
        try:
            await user.send(f"Hello User `{username}`, Please provide your valid `GCash phone number` before proceeding.")
            await interaction.response.send_message("I've sent you a DM with further instructions!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I couldn't send you a DM. Please check your DM settings.", ephemeral=True)
