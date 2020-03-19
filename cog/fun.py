import discord
import re
import random
import requests
import asyncio
from discord.ext import commands
from bs4 import BeautifulSoup

class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def roll(self, ctx, *, msg="6"):
        """Roll dice. """
        dice_rolls = []
        dice_roll_ints = []
        try:
            dice, sides = re.split("[d]", msg)
        except ValueError:
            sides = msg
            dice = "1"
        try:
            for roll in range(int(dice)):
                result = random.randint(1, int(sides))
                dice_rolls.append(str(result))
                dice_roll_ints.append(result)
        except ValueError:
            return await ctx.send(self.bot.bot_prefix + "Invalid Syntax")

        embed = discord.Embed(title="Dice rolls:", description=' '.join(dice_rolls))
        embed.add_field(name="Total: ", value=sum(dice_roll_ints))
        await ctx.send("", embed= embed)

    async def fetch_data(self, url):
        r= requests.get(url)
        await asyncio.sleep(3)
        return r


    @commands.command()
    async def corona(self, ctx, *, country):
        r = await self.fetch_data('https://www.worldometers.info/coronavirus/')
        if r is not None:
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find(id="main_table_countries_today")
            child = list(table.children)[3]
            print(child)
    

    




def setup(client):
    client.add_cog(Fun(client))