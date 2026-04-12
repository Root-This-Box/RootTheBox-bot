import discord
import os
from dotenv import load_dotenv

INTENTS = discord.Intents.default()
INTENTS.message_content = True

GUILD_ID=1492689366999498762

load_dotenv()
BOT_TOKEN=os.getenv("BOT_TOKEN")

APPLICATION_ID=os.getenv("APP_ID")