import discord
from discord import app_commands
from discord.ext import commands
from os import environ


class User(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="register", description="Register as a user")
    async def register(self, interaction: discord.Interaction, gcash_number: str):
        await interaction.response.send_message(
            f"Your gcash number is {gcash_number}, correct?\n**This cannot be changed after confirming**",
            view=GCashConfirmView(gcash_number),
            ephemeral=True,
        )

    @app_commands.command(name="unregister", description="Unregister as a user")
    async def unregister(self, interaction: discord.Interaction): ...


class GCashConfirmView(discord.ui.View):
    def __init__(self, gcash: str):
        super().__init__()
        self.gcash = gcash
        self.interacted = False

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

    @discord.ui.button(label="yes", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, _button: discord.ui.Button
    ):
        if not self.interacted:
            await interaction.response.send_message(
                content=f"You have confirmed that {self.gcash} is your phone number",
                ephemeral=True,
            )

        self.interacted = True

    @discord.ui.button(label="no", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if not self.interacted:
            await interaction.response.send_message(
                content="You have cancelled the operation", ephemeral=True
            )

        self.interacted = True


async def setup(bot: commands.Bot):
    await bot.add_cog(User(bot), guild=discord.Object(environ["BOT_GUILD_ID"]))
