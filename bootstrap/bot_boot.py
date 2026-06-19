import discord
from bootstrap.intents import *
from discord.ext import commands

version = "v1.0.0"

# Custom bot subclass for SmokeUtils.
class SmokeUtils(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="su!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Called during bot startup to sync application commands.
        await self.tree.sync()
        print("commands synced")

bot = SmokeUtils()

@bot.event
async def on_ready():
    # Called once when the bot successfully connects to Discord.
    global server_count
    server_count = len(bot.guilds)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f'InkUtils {version}'))
    print("running")
