import discord
from discord.ext import commands
from discord import app_commands
from bot.bot_config import GUILD_ID

class other_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="credits", description="Give credit to everyone who worked on the bot!")
    async def credits(self, interaction: discord.Interaction):
        await interaction.response.send_message("""
        Credits go to: 
    wired8, for helping on creating the bot and the RootThisBox website!
    therealrealystupid, for creating the discord bot you see today alongside his hacking journey!
                                       
QUICK NOTE FROM therealrealystupid: im kinda broke and working on bot and trying to teach myself hacking is kinda hard to do lol
    so if you have money to spare please concider sending me a small some of bitcoin to me! only if u want tho, not forcing u
    `bc1q27el8z637ll8p4flamztqwwmdpj79may3m0krl`
                                
thanks for being a part of this community and keep on hacking!
        """)


async def setup(bot):
    cog = other_commands(bot)
    bot.tree.add_command(cog.credits, guild=discord.Object(id=GUILD_ID))
    await bot.add_cog(cog)