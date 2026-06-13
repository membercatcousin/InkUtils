import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# Simple command that replies with a short, fixed message.
@bot.hybrid_command(name="tjwt", description="The jokes write themselves at this point.")
async def dont_ask(ctx):
    await ctx.send("The jokes write themselves at this point. 💔:wilted_rose:")
