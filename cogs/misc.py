import nextcord
from nextcord.ext import commands
import random

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rolldice", description="Roll a dice")
    async def roll(self, ctx, sides: int = 6):
        """Rolls a dice with the given number of sides (default is 6)."""
        result = random.randint(1, sides)
        await ctx.send(f'🎲 You rolled a {result} on a {sides}-sided dice!')

    @commands.command(name="ping", description="Check bot's latency")
    async def ping(self, ctx):
        """Sends the bot's latency."""
        latency = round(self.bot.latency * 1000)  # Convert to ms
        await ctx.send(f'🏓 Pong! Latency is {latency}ms')

    @commands.command(name="say", description="Make the bot say something")
    async def say(self, ctx, *, message: str):
        """Repeats what you say."""
        await ctx.send(message)

    @commands.command(name="choose", description="Choose between multiple options")
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple options."""
        if len(choices) < 2:
            await ctx.send("You need to provide at least two options to choose from.")
        else:
            choice = random.choice(choices)
            await ctx.send(f'I choose: {choice}')

def setup(bot):
    bot.add_cog(Misc(bot))
