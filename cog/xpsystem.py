import discord
from discord.ext import commands,tasks
import pymongo

class XPSystem(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.mongo = self.client.mongo_client["Rimuru"]
        self.xp = self.mongo["XP"]

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.author == self.client.user:
            return
        
        if msg.channel is not discord.DMChannel:
            exists = await self.user_check(msg.author)
            if exists is not None:
                query = {"_id": msg.author.id}
                newval = { "$set": { "XP": exists["XP"] + 1, "RimuCoins": exists["RimuCoins"] + 1}}
                self.xp.update_one(query, newval)

            if self.check_level(exists):
                await self.level_up(msg.channel, exists, msg.author)
    
    @commands.command()
    async def profile(self, ctx):
        data = await self.user_check(ctx.author)
        embed = discord.Embed(
            title = f"{ctx.author.name}'s stats",
            colour = discord.Colour.blue()
        )
        xp = data["XP"]
        lvl = data["Level"]
        coins = data["RimuCoins"]
        embed.add_field(name="Level", value=lvl, inline=True)
        embed.add_field(name="XP", value=f"{xp} / {self.next_level(lvl)}", inline=True)
        embed.add_field(name="RimuCoins", value=coins, inline=True)
        await ctx.send(embed=embed)
        

    @commands.command()
    @commands.is_owner()
    async def reset_data(self, ctx, user:discord.Member):
        query = {"_id": user.id}
        newval = { "$set": { "XP": 1, "Level": 1, "RimuCoins": 100}}
        self.xp.update_one(query, newval)
        await ctx.send(f"{user.name}'s data has been reset!")

        
    def check_level(self, user):
        xp_needed = self.next_level(user["Level"])
        if user["XP"]+1 > xp_needed:
            return True

    def next_level(self,level):
        return 2 * (level**3)

    async def level_up(self,channel : discord.TextChannel, data, user:discord.Member):
        query = {"_id": data["_id"] }
        newval = { "$set": { "Level": data["Level"] + 1, "RimuCoins": data["RimuCoins"] + 100}}
        self.xp.update_one(query, newval)
        embed = discord.Embed(description=f'{user.mention} leveled up! level {data["Level"]+1} ', colour = discord.Colour.blue())
        await channel.send(embed=embed)

    async def user_check(self, dUser : discord.Member):
        cmd = {"_id": dUser.id}
        exists = self.xp.count_documents(cmd)
        if exists < 1:
            cmd = {"_id": dUser.id, "XP": 1, "Level": 1, "RimuCoins": 100}
            self.xp.insert_one(cmd)

        cmd = {"_id": dUser.id}
        exists_again = self.xp.find(cmd)
        return exists_again[0]


def setup(client):
    client.add_cog(XPSystem(client))