import discord
import praw
import praw.exceptions 
import random
from discord.ext import commands

#SomeStronmgPassword13324

class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id='LnPsISq2_IKTcA',
                     client_secret='hz0fD0dha2cLfV-Czv-CkMzT1aE',
                     password='SomeStronmgPassword13324',
                     user_agent='testscript by /u/Rimuru_DS',
                     username='Rimuru_DS')
        self.nsfw_list = ["collegesluts", "petite", "nsfw", "milf", "gonewild18", "amateur", "normalnudes", 
                              "AsiansGoneWild", "rule34", "ecchi", "furry", "monstergirl", "hentai_gif", "hentai", "rule34lol",
                              "bdsm", "femdom", "blowjobs", "deepthroat", "ass", "buttplug", "anal", "boobs", "nipples", 
                              "tinytits", "blonde", "stockings", "tighyshorts", "feet", "pussy"]
        self.nsfw_list.sort()

    @commands.command()
    async def nsfw(self,ctx, *, category):
        """ There are 3 commands ./nsfw [list, random or category from list]"""
        if ctx.channel.is_nsfw():
            if category == "list":
                await self.tag_list(ctx)
            elif category == "random":
                await self.send_image(ctx, random.choice(self.nsfw_list))
            else:
                if category in self.nsfw_list:
                    await self.send_image(ctx, category)
        else:
            await ctx.send(" You need to enable **NSFW** for this channel!")
    
    @commands.command()
    @commands.has_any_role('Super Member', 'Admin')
    async def nsfw_add(self,ctx, category):
        """ Temporarily adds new nsfw subreddit"""
        if ctx.channel.is_nsfw():
            if category is not None:
                if self.sub_exists(category):
                    if category not in self.nsfw_list:
                        self.nsfw_list.append(category)
                        await ctx.send("Category **"+category+"** has been added to the list!")

    async def tag_list(self,ctx):
        string = ""
        for i in self.nsfw_list:
            string+= "**"+str(i)+"**"  + ",  "

        string = string[:-2]
        string += "."
        embed = discord.Embed(
            title = "Tags",
            description = string,
            colour = discord.Colour.blue()
        )

        await ctx.send(embed=embed)

    def sub_exists(self,sub):
        exists = True
        try:
            self.reddit.subreddits.search_by_name(sub, exact=True)
        except praw.exceptions.ClientException:
            exists = False
        return exists
    
    async def send_image(self,ctx, category):
        post = self.reddit.subreddit(category).random()
        url = (post.url) #Check for gifycat and extract the file from it
        embed = discord.Embed(
            title= post.title,
            colour = discord.Colour.blue()
        )

        embed.set_image(url=url)
        await ctx.send(embed=embed)

        

def setup(client):
    client.add_cog(Reddit(client))


