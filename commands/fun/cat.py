import discord
import random
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# List of cat image URLs used by the cat command.
cats = [
    "https://cataas.com/cat",
    "https://cataas.com/cat/orange",
    "https://cataas.com/cat/says/hi",
    "https://cataas.com/cat/says/hello",
    "https://cataas.com/cat/says/meow",
    "https://cataas.com/cat/says/purr",
    "https://cataas.com/cat/says/miw",
    "https://cataas.com/cat/says/nya",
    "https://cataas.com/cat/says/nyaa",
    "https://cataas.com/cat/cute",
    "https://cataas.com/cat/duo",
    "https://cataas.com/cat/gif"
]

@bot.hybrid_command(name="cat", description="Send a random cat picture")
async def cat(ctx):
    # Reply with a random cat image URL from the list.
    await ctx.reply(random.choice(cats))
