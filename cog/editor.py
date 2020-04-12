import discord
import os
from discord.ext import commands

class Editor(commands.Cog):
    def __init(self, client):
        self.client = client
    

    @commands.command()
    @commands.is_owner()
    async def showFile(self,ctx, file_name):
        for filename in os.listdir('./cog'):
            if filename[:-3] == file_name:
                print("found file "+filename)
                file = open("./cog/"+file_name+".py", "r")
                await ctx.send("```python\n"+file.read()+"```")


def setup(client):
    client.add_cog(Editor(client))