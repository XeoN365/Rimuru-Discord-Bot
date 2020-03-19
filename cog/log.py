import discord

from discord.ext import commands

class Logger(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def discordLog(self,ctx, exception : str):
        reaction = self.client.get_cog('Reaction')
        await ctx.send(f'{reaction.fail} {exception}')


def setup(client):
    client.add_cog(Logger(client))