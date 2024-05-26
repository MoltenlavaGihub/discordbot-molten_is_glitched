# voice.py

import nextcord
from nextcord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", description="Make the bot join the voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            return
        
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()
        
        await ctx.send(f"Joined {voice_channel.name}")

    @commands.command(name="leave", description="Make the bot leave the voice channel")
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel")
        else:
            await ctx.send("I am not in a voice channel")

def setup(bot):
    bot.add_cog(Voice(bot))
 
