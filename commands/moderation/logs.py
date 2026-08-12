import discord
from discord.ext import commands
from bootstrap.bot_boot import *
from logic.logs import get_log_channel_id, set_log_channel_id, remove_log_channel

# Utility to resolve the configured log channel for a guild.
async def _get_log_channel(guild: discord.Guild):
    ch_id = get_log_channel_id(guild.id)
    if not ch_id:
        return None

    ch = guild.get_channel(ch_id)
    if ch is None:
        ch = bot.get_channel(ch_id)
    if ch is None:
        try:
            ch = await guild.fetch_channel(ch_id)
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            return None

    if isinstance(ch, discord.TextChannel):
        return ch
    return None

# Group commands for moderation logs management.
@bot.hybrid_group(name="logs", description="Manage moderation logs")
@commands.has_permissions(manage_guild=True)
async def logs_group(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.reply("Use `/logs setup` to set the logs channel or `/logs disable` to disable logs.")

@logs_group.command(name="setup", description="Set the moderation logs channel")
@commands.has_permissions(manage_guild=True)
async def logs_setup(ctx: commands.Context, channel: discord.TextChannel):
    # Set the log channel for this guild.
    set_log_channel_id(ctx.guild.id, channel.id)
    await ctx.reply(f"Logs channel set to {channel.mention}")

@logs_group.command(name="disable", description="Disable moderation logs")
@commands.has_permissions(manage_guild=True)
async def logs_disable(ctx: commands.Context):
    # Disable logs posting for this guild.
    remove_log_channel(ctx.guild.id)
    await ctx.reply("Moderation logs have been disabled.")

@bot.event
async def on_message_delete(message: discord.Message):
    if message.guild is None or message.author.bot:
        return
    ch = await _get_log_channel(message.guild)
    if not ch:
        return
    embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
    embed.add_field(name="Author", value=f"{message.author} ({message.author.id})", inline=False)
    embed.add_field(name="Channel", value=message.channel.mention, inline=False)
    embed.add_field(name="Content", value=message.content[:1000] if message.content else "<no content>", inline=False)
    embed.timestamp = discord.utils.utcnow()
    await ch.send(embed=embed)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if after.guild is None or after.author.bot or before.content == after.content:
        return
    ch = await _get_log_channel(after.guild)
    if not ch:
        return
    embed = discord.Embed(title="Message Edited", color=discord.Color.orange())
    embed.add_field(name="Author", value=f"{after.author} ({after.author.id})", inline=False)
    embed.add_field(name="Channel", value=after.channel.mention, inline=False)
    embed.add_field(name="Before", value=before.content[:1000] if before.content else "<no content>", inline=False)
    embed.add_field(name="After", value=after.content[:1000] if after.content else "<no content>", inline=False)
    embed.timestamp = discord.utils.utcnow()
    await ch.send(embed=embed)

@bot.event
async def on_member_remove(member: discord.Member):
    if member.guild is None:
        return
    ch = await _get_log_channel(member.guild)
    if not ch:
        return
    embed = discord.Embed(title="Member Left", description=f"{member} ({member.id})", color=discord.Color.dark_gray())
    embed.timestamp = discord.utils.utcnow()
    await ch.send(embed=embed)
