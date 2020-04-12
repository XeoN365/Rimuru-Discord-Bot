import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def purge(self, ctx, amount = 10):
        async with ctx.channel.typing():
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.send(f"Deleted {len(deleted)} messages!", delete_after = 5)
    
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason = 'No Reason'):
        async with ctx.channel.typing():
            
            await member.kick(reason=reason)
            
            await ctx.send(f"{member.mention} has been kicked! Reason: {reason}")

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason = 'No Reason'):
        async with ctx.channel.typing():
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned! Reason: {reason}")

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def unban(self, ctx, *member : str):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"User {user.mention} has been unbanned!")
                return
    @commands.has_permissions(ban_members=True)
    @commands.command(aliases=["allBans","banList"])
    async def all_bans(self, ctx):
        users = ""
        bannedList = await ctx.guild.bans()

        for entry in bannedList:
            user = entry.user
            users+= f"{user.name}#{user.discriminator} "
        
        await ctx.send(f"**Banned users list:** ```{users}```")

def setup(client):
    client.add_cog(Moderation(client))
