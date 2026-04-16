import discord
from discord.ext import commands
from llama3.ai import x_inst, linkedin_inst, ai_call

class Llama3Calling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create")
    async def ai_call(self, ctx, platform: str):
        if ctx.prefix == "?":
            if platform.lower() == "x" or platform.lower() == "twitter" or platform.lower() == "x.com":
                await ctx.send("Provide a prompt for X/Twitter in your next message.")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                
                reply = await self.bot.wait_for('message', check=check)
                await ctx.send("Generating response...")
                
                async with ctx.typing():
                    instructions = await x_inst()
                    response = await ai_call(instructions, reply.content)
                    await ctx.send(response)

            elif platform.lower() == "linkedin":
                await ctx.send("Provide a prompt for LinkedIn in your next message.")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                
                reply = await self.bot.wait_for('message', check=check)
                await ctx.send("Generating response...")
                
                async with ctx.typing():
                    instructions = await linkedin_inst()
                    response = await ai_call(instructions, reply.content)
                    await ctx.send(response)

        

async def setup(bot):
    await bot.add_cog(Llama3Calling(bot))