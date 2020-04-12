import os
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
import pymongo
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USERNAME = os.getenv('MONGO_USER')
PASS = os.getenv('MONGO_PASS')
CLUSTER = os.getenv('CLUSTER_URL')


def find_prefix(guild_id):
    query = { "guild_id" : guild_id}
    result = prefixes_db.find(query)
    return result[0]

def get_prefix(client, message):
    if message.guild is not None:
        prefix = find_prefix(message.guild.id)
        return prefix["prefix"]
    else:
        return "./"
    

client = commands.Bot(command_prefix= get_prefix)
client.mongo_client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASS}@{CLUSTER}/test?retryWrites=true&w=majority")
rimuru_db = client.mongo_client["Rimuru"]
prefixes_db = rimuru_db["Prefixes"]

directory = os.getcwd()

# EVENTS

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    guilds = client.guilds
    for guild in guilds:
        cmd = { "guild_id": guild.id}
        exists = prefixes_db.count_documents(cmd)
        if exists < 1:
            cmd = { "guild_id": guild.id, "prefix": "./"}
            prefixes_db.insert_one(cmd)


@client.event
async def on_guild_join(guild):
    template = { "guild_id": guild.id, "prefix": "./" }
    prefixes_db.insert_one(template)

@client.event
async def on_guild_remove(guild):
    template = { "guild_id": guild.id }
    prefixes_db.delete_one(template)

@client.event
async def on_command(ctx):
    reaction = client.get_cog('Reaction')
    await ctx.message.add_reaction(reaction.success)

@client.event
async def on_command_error(ctx, err):
    logger = client.get_cog('Logger')
    reaction = client.get_cog('Reaction')
    await ctx.message.add_reaction(reaction.fail)
    await logger.discordLog(ctx,err)
    print(err)

# Level-0 Commands

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    
    """Loads an extension (cog)"""
    reaction = client.get_cog('Reaction')
    client.load_extension(f'cog.{extension}')
    await ctx.send(f"{reaction.success} *`cog.{extension}`* has been loaded!")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Unloads an extension (cog)"""
    client.unload_extension(f'cog.{extension}')
    reaction = client.get_cog('Reaction')
    await ctx.send(f"{reaction.success} *`cog.{extension}`* has been unloaded!")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Reloads an extension (cog)"""
    if f'cog.{extension}' in client.extensions:
        client.unload_extension(f'cog.{extension}')

    client.load_extension(f'cog.{extension}')
    reaction = client.get_cog('Reaction')
    await ctx.send(f"{reaction.success} *`cog.{extension}`* has been reloaded!")

@client.command()
@commands.has_permissions(manage_guild=True)
async def changeprefix(ctx, prefix):
    query = { "guild_id": ctx.guild.id }
    newval = { "$set": { "prefix" : prefix}}
    prefixes_db.update_one(query, newval)
    await ctx.send(f"Prefix `{prefix}` has been set!")



for filename in os.listdir('./cog'):
    if filename.endswith('.py'):
        client.load_extension(f'cog.{filename[:-3]}')
        print(f'{filename[:-3]} has loaded!')

client.run(TOKEN)
 