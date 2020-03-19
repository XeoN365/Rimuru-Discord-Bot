import discord
from discord.ext import commands

class Reaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    success = "✅"
    fail = "❌"

def setup(client):
    client.add_cog(Reaction(client))