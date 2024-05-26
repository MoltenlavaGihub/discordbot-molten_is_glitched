# In your main script (e.g., bot.py)
import nextcord
import config
import aiohttp
import asyncio
from nextcord.ext import commands

# Create bot instance with appropriate intents
intents = nextcord.Intents.default()
intents.voice_states = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='.', intents=intents)

# Load cogs
bot.load_extension('cogs.fun')
bot.load_extension('cogs.voice')
bot.load_extension('cogs.moderation')
bot.load_extension('cogs.roll') 
bot.load_extension('cogs.misc') 
bot.load_extension('cogs.utility')
bot.load_extension('cogs.economy') 
bot.load_extension('cogs.quotes')
bot.load_extension('cogs.fight')


# Run the bot
bot.run(config.BOT_TOKEN)
