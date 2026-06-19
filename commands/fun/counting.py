import discord
from discord import app_commands
from discord.ext import commands
from bootstrap.bot_boot import *
from logic.counting import get_counting_channel_id, set_counting_channel_id, remove_counting_channel, get_last_count, set_last_count, get_last_user_id, set_last_user_id
from logic.leveling import get_leveling_enabled, get_xp_gain, add_xp, get_role_for_level, get_announce_channel_id

@bot.hybrid_group(name="counting", description="Manage counting feature")
@commands.has_permissions(manage_guild=True)
async def counting_group(ctx: commands.Context):
    # Root command group for counting setup commands.
    pass

@counting_group.command(name="setup", description="Set the counting channel")
@commands.has_permissions(manage_guild=True)
async def setup(ctx: commands.Context, channel: discord.TextChannel):
    # Set the counting channel for this guild and initialize state.
    set_counting_channel_id(ctx.guild.id, channel.id)
    await ctx.reply(f"Counting channel set to {channel.mention}. Start counting from 1!")

@counting_group.command(name="disable", description="Disable counting feature")
@commands.has_permissions(manage_guild=True)
async def disable(ctx: commands.Context):
    # Disable the counting feature by removing stored guild state.
    remove_counting_channel(ctx.guild.id)
    await ctx.reply("Counting feature disabled.")

@bot.event
async def on_message(message):
    # Ignore messages sent by bots.
    if message.author.bot:
        return
    
    # Only proceed if message is in a guild.
    if message.guild is None:
        return
    
    guild_id = message.guild.id
    
    # Counting system logic
    ch_id = get_counting_channel_id(guild_id)
    # Only process counting messages in the configured channel.
    if ch_id and message.channel.id == ch_id:
        last_user = get_last_user_id(guild_id)
        # Do not allow the same user to count twice in a row.
        if last_user and message.author.id == last_user:
            await message.delete()
            return
        
        last = get_last_count(guild_id)
        try:
            num = int(message.content.strip())
            # Accept only the next integer in the sequence.
            if num == last + 1:
                set_last_count(guild_id, num)
                set_last_user_id(guild_id, message.author.id)
                await message.add_reaction("✅")
            else:
                await message.delete()
        except ValueError:
            # Remove any non-integer messages from the counting channel.
            await message.delete()
    
    # Leveling system logic
    if get_leveling_enabled(guild_id):
        xp_gain = get_xp_gain(guild_id)
        new_level = add_xp(guild_id, message.author.id, xp_gain)
        
        # Notify the user if they leveled up and assign any associated roles.
        if new_level is not None:
            embed = discord.Embed(
                title="Level Up!",
                description=f"{message.author.mention} reached **Level {new_level}**! 🎉",
                color=discord.Color.green()
            )
            announce_channel_id = get_announce_channel_id(guild_id)
            if announce_channel_id:
                announce_channel = message.guild.get_channel(announce_channel_id)
                if announce_channel is not None:
                    try:
                        await announce_channel.send(embed=embed)
                    except discord.Forbidden:
                        await message.reply(embed=embed, mention_author=False)
                else:
                    await message.reply(embed=embed, mention_author=False)
            else:
                await message.reply(embed=embed, mention_author=False)
            
            # Assign role if one is configured for this level.
            role_id = get_role_for_level(guild_id, new_level)
            if role_id:
                role = message.guild.get_role(role_id)
                if role:
                    try:
                        await message.author.add_roles(role)
                    except discord.Forbidden:
                        await message.reply("I don't have permission to assign roles.", mention_author=False)
    
    # Continue processing commands after message handling.
    await bot.process_commands(message)