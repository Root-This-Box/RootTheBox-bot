# the main entrypoint for the bot
import asyncio
import subprocess
import discord
from discord.ext import commands

import os
import bot.bot_config as config

async def get_prefix(bot, message):
    # This function can be used to get a dynamic prefix based on the guild or other factors
    prefix = ["!"]  # default prefix
    
    # if the author of the command is an admin this is the prefix they will use
    if message.author.guild_permissions.administrator:
        prefix.append("?")  # admin prefix
    
    return prefix

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=config.INTENTS, application_id=config.APPLICATION_ID)

    async def setup_hook(self):
        print("[SETUP HOOK] The setup_hook has started")
        print("----------------------------------------------------------------------")

        await self.load_cogs_recursively()

        print("\n")
        await self.turn_ai_on()

        print("----------------------------------------------------------------------")
        print("[SETUP HOOK] setup_hook has completed")
    
    async def load_cogs_recursively(self, root="bot/cogs"):
        root = root.replace("\\", "/")  # normalize path

        for dirpath, _, filenames in os.walk(root):
            module_base = dirpath.replace("/", ".")

            for filename in filenames:
                if not filename.endswith(".py"):
                    continue

                # Reject files containing "_" at the begining
                if filename.startswith("_"):
                    continue

                module_name = filename[:-3]
                extension_path = f"{module_base}.{module_name}"

                try:
                    await bot.load_extension(extension_path)
                    print(f"[COG LOADER] Loaded cog: {extension_path}")
                except Exception as e:
                    print(f"[COG LOADER] Failed to load {extension_path}: {e}")

    async def turn_ai_on(self):
        #check if the ai is already on
        proc = await asyncio.create_subprocess_shell(
            "pgrep ollama",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()

        if stdout:
            print("[AI] Ollama is already running.")
            return
        
        print("[AI] Starting Ollama...")
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        await asyncio.sleep(30)  # Wait a bit for Ollama to start
        print("[AI] Ollama should now be running.")

    async def on_ready(self):
        print("----------------------------------------------------------------------")
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