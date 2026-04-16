import discord
from discord.ext import commands
from llama3.x.x_post import ai_call

class Llama3Calling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_x_post")
    async def create_x_post(self, ctx, prompt: str):
        if ctx.prefix == "?":
            async with ctx.typing():
                response = await ai_call(prompt)
                await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Llama3Calling(bot))