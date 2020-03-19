import discord
from discord.ext import commands

class Info(commands.Cog): 
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def ping(self, ctx):
        reaction = self.client.get_cog('Reaction')
        await ctx.send(f'{reaction.success} Pong! {round(self.client.latency * 1000)}ms')

def setup(client):
    client.add_cog(Info(client))
