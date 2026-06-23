import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# Simple command that replies with a short, fixed message.
@bot.hybrid_command(name="aa", description="Absolute Cinema")
async def dont_ask(ctx):
    await ctx.send("https://tenor.com/view/absolute-cinema-absolute-cinema-meme-absolute-membercatcousin-gif-13890029056599638238")
