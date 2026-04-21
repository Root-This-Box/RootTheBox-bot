# the main entrypoint for the bot
import asyncio
import subprocess
import discord
from discord.ext import commands
import socket
import os
import bot.bot_config as config

def is_distrobox():
    #this just checks if the user is running the program inside the distrobox
    if os.environ.get("DISTROBOX") == "1":
        return True
    if os.environ.get("container") == "distrobox":
        return True
    if os.path.exists("/run/.containerenv"):
        return True
    if "distrobox" in socket.gethostname() or "toolbox" in socket.gethostname():
        return True
    return False

async def get_prefix(bot, message):
    # This function can be used to get a dynamic prefix based on the guild or other factors
    prefix = ["!"]  # default prefix
    
    # if the author of the command is an admin this is the prefix they will use
    if message.author.guild_permissions.administrator:
        prefix.append("?")  # admin prefix
    
    return prefix

async def wait_for_ollama_ready(timeout=20):
    """Poll the host's Ollama server until it's ready or timeout."""
    start = asyncio.get_event_loop().time()

    while True:
        # Try hitting the host's Ollama server
        proc = await asyncio.create_subprocess_shell(
            "distrobox-host-exec curl -s http://localhost:11434/api/tags",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()

        if stdout:  # Any JSON response means Ollama is alive
            return True

        # Timeout check
        if asyncio.get_event_loop().time() - start > timeout:
            return False

        await asyncio.sleep(0.5)  # Poll every 500ms

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=config.INTENTS, application_id=config.APPLICATION_ID)

    async def setup_hook(self):
        print("[SETUP HOOK] The setup_hook has started")
        print("----------------------------------------------------------------------")
        if is_distrobox():
            print("[DISTRO BOX CHECKER] The enviroment is within a distrobox.\n__________________________________________")
        await self.load_cogs_recursively()
        print("__________________________________________")
        # await self.turn_ai_on()

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
        # Check if Ollama is already running on the host
        if is_distrobox():
            proc = await asyncio.create_subprocess_shell(
                "distrobox-host-exec pgrep ollama",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        else:
            proc = await asyncio.create_subprocess_shell(
                "pgrep ollama",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        stdout, _ = await proc.communicate()

        if stdout:
            print("[AI] Ollama is already running. Checking readiness...")
            ready = await wait_for_ollama_ready()
            print("[AI] Ollama ready." if ready else "[AI] Ollama not responding.")
            return

        print("[AI] Starting Ollama...")
        if is_distrobox():
            subprocess.Popen(
                ["distrobox-host-exec", "ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        print("[AI] Waiting for Ollama to become ready...")
        ready = await wait_for_ollama_ready()

        if ready:
            print("[AI] Ollama is ready to use.")
        else:
            print("[AI] ERROR: Ollama did not start in time.")

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