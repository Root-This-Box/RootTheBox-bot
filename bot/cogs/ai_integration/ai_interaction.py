import discord
from discord.ext import commands, tasks
import datetime
from llama3.ai import discord_announcement_inst, x_inst, linkedin_inst, daily_announcement_inst, random_words, ai_call

TARGET_HOUR = 12
TARGET_MINUTE = 0

class Llama3Calling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduled_ai_call.start()

    @commands.command(name="create")
    async def create_request(self, ctx, type: str):
        if ctx.prefix == "?":
            if type.lower() == "x" or type.lower() == "twitter" or type.lower() == "x.com":
                await ctx.send("Provide a prompt for X/Twitter in your next message.")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                
                reply = await self.bot.wait_for('message', check=check)
                await ctx.send("Generating response...")
                
                async with ctx.typing():
                    instructions = await x_inst()
                    response = await ai_call(instructions, reply.content)
                    await ctx.send(response)

            elif type.lower() == "linkedin":
                await ctx.send("Provide a prompt for LinkedIn in your next message.")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                
                reply = await self.bot.wait_for('message', check=check)
                await ctx.send("Generating response...")
                
                async with ctx.typing():
                    instructions = await linkedin_inst()
                    response = await ai_call(instructions, reply.content)
                    await ctx.send(response)

            elif type.lower() == "discord" or type.lower() == "announcement":
                channel = self.bot.get_channel(1492695797827899402)

                await ctx.send("Provide a prompt for a Discord announcement in your next message.")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                
                reply = await self.bot.wait_for('message', check=check)
                await ctx.send("Generating response...")
                
                async with ctx.typing():
                    instructions = await discord_announcement_inst()
                    response = await ai_call(instructions, reply.content)
                    await channel.send(response)

    @commands.command(name="daily_test")
    async def daily_test(self, ctx):
        if ctx.prefix == "?":
            channel = self.bot.get_channel(1494840441407803472)

            full_instructions = await daily_announcement_inst() + "\n" + await random_words("llama3/wordlist.txt", 10)
                
            response = await ai_call(full_instructions)

            await channel.send(response)
        
    @tasks.loop(minutes=1)
    async def scheduled_ai_call(self):
        now = datetime.datetime.now()
        if now.hour == TARGET_HOUR and now.minute == TARGET_MINUTE:
            channel = self.bot.get_channel(1494840441407803472)

            full_instructions = await daily_announcement_inst() + "\n" + await random_words("llama3/wordlist.txt", 10)

            response = await ai_call(full_instructions)

            await channel.send(response)

    @scheduled_ai_call.before_loop
    async def before_scheduled_ai_call(self):
        print("Waiting for bot to be ready before starting scheduled AI calls...")
        await self.bot.wait_until_ready()
        print("Bot is ready. Starting scheduled AI calls.")


async def setup(bot):
    await bot.add_cog(Llama3Calling(bot))