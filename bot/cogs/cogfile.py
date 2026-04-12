import discord
from discord.ext import commands
from discord import app_commands
from bot.bot_config import GUILD_ID

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='test', description='A simple test command')
    async def test_command(self, interaction: discord.Interaction):
        """A basic test command"""
        await interaction.response.send_message(f'Hello {interaction.user.name}! This is a test command.')


async def setup(bot):
    cog = TestCog(bot)
    bot.tree.add_command(cog.test_command, guild=discord.Object(id=GUILD_ID))
    await bot.add_cog(cog)