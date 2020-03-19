import os
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix= './')
directory = os.getcwd()

# EVENTS

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_command(ctx):
    reaction = client.get_cog('Reaction')
    await ctx.message.add_reaction(reaction.success)

@client.event
async def on_command_error(ctx, err):
    logger = client.get_cog('Logger')
    await logger.discordLog(ctx,err)
    print(err)

# Level-0 Commands

@client.command()
@commands.has_any_role(*["Admin"])
@commands.has_permissions(administrator=True )
async def load(ctx, extension):
    """Loads an extension (cog)"""
    reaction = client.get_cog('Reaction')
    client.load_extension(f'cog.{extension}')
    await ctx.send(f"{reaction.success} *`cog.{extension}`* has been loaded!")

@client.command()
@commands.has_any_role(*["Admin"])
@commands.has_permissions(administrator=True )
async def unload(ctx, extension):
    """Unloads an extension (cog)"""
    client.unload_extension(f'cog.{extension}')
    reaction = client.get_cog('Reaction')
    await ctx.send(f"{reaction.success} *`cog.{extension}`* has been unloaded!")

@client.command()
@commands.has_any_role(*["Admin"])
@commands.has_permissions(administrator=True )
async def reload(ctx, extension):
    """Reloads an extension (cog)"""
    if f'cog.{extension}' in client.extensions:
        client.unload_extension(f'cog.{extension}')

    client.load_extension(f'cog.{extension}')
    reaction = client.get_cog('Reaction')
    await ctx.send(f"{reaction.success} *`cog.{extension}`* has been reloaded!")

for filename in os.listdir('./cog'):
    if filename.endswith('.py'):
        client.load_extension(f'cog.{filename[:-3]}')
        print(f'{filename[:-3]} has loaded!')

client.run(TOKEN)
