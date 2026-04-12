# the main entrypoint for the bot
import discord
from discord.ext import commands

import os

import bot.bot_config as config

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=config.INTENTS, application_id=config.APPLICATION_ID)

    async def setup_hook(self):
        print("[SETUP HOOK] The setup hook has started")

    async def on_ready(self):
        print(f"logged in: {self.user}")

bot = Client()

@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    try:
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} commands to **{ctx.guild.name}**")
    except Exception as e:
        await ctx.send(f"Error while syncing commands: `{e}`")

bot.run(config.BOT_TOKEN)