import discord
from discord.ext import commands

TARGET_REACTION = "💀"
THRESHHOLD = 5
CHANNEL_ID = 1495806631940984882

class reaction_listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        
        if str(payload.emoji) != TARGET_REACTION:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return
        
        message = await channel.fetch_message(payload.message_id)
        
        skull_count = 0
        for reaction in message.reactions:
            if str(reaction.emoji) == TARGET_REACTION:
                skull_count = reaction.count
                break

        if skull_count == THRESHHOLD:
            return
        
        skullboard_channel = self.bot.get_channel(CHANNEL_ID)
        if skullboard_channel is None:
            return
        
        embed = discord.Embed(
            title="💀 Skullboard Entry",
            description=message.content or "*No text content*",
            color=discord.Color.dark_gray()
        )

        embed.add_field(
            name="Author",
            value=message.author.mention,
            inline=True
        )

        embed.add_field(
            name="Jump to Message",
            value=f"[Click Here]({message.jump_url})",
            inline=True
        )

        # If message has an image attachment, include it
        if message.attachments:
            first = message.attachments[0]
            if first.content_type and first.content_type.startswith("image/"):
                embed.set_image(url=first.url)

        await skullboard_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(reaction_listener(bot))