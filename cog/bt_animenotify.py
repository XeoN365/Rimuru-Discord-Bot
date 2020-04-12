import discord
from discord.ext import commands, tasks
import pymongo
import requests
from bs4 import BeautifulSoup

class AnimeNotify(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rimuru = client.mongo_client["Rimuru"]
        self.anime = self.rimuru["AnimeNotify"]
        self.previous_list = list([])
        self.anime_loop.start()

    def cog_unload(self):
        self.anime_loop.cancel()
    

    async def getWebsiteData(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        t = soup.find('div', class_="last_episodes")
        mainList = t.find('ul')
        itemlist = mainList.find_all('li')
        return itemlist

    @tasks.loop(minutes=30)
    async def anime_loop(self):
        url = 'https://www2.gogoanime.video'
        cursor = self.anime.find({})
        anime_list = await self.getWebsiteData(url)
        itemlist = list()
        update = list()
        for item in anime_list: 

            raw_anime_name = item.find('a').get('title')
            lower_anime_name = raw_anime_name.lower()
            img_url = item.find('img').get('src')
            anime_link = url+item.find('a').get('href')

            new_anim = { "raw_name": raw_anime_name, 
                         "name": lower_anime_name,
                         "img": img_url,
                         "link": anime_link }
            
            if new_anim not in self.previous_list:
                update.append(new_anim)

            itemlist.append(new_anim)
        if len(update) > 0:
            for document in cursor:
                if document["animeList"] is not None:
                    for animel in document["animeList"]:
                        for anime in update:
                            if anime["name"] == animel.lower():
                                user = self.client.get_user(document["_id"])
                                embed = discord.Embed(description="New episode of "+anime["raw_name"]+"is out! watch it [here]("+anime["link"]+")", colour= discord.Colour.blue())
                                embed.set_image(url=anime["img"])
                                await user.send(embed=embed)

        self.previous_list = itemlist

    @commands.command()
    async def anime_test(self,ctx):
        await self.anime_loop(ctx)

    @commands.command()
    async def add_anime(self,ctx, *, anime):
        query = { "_id": ctx.author.id}
        current = self.anime.count_documents(query)
        if current > 0:

            cur = list(self.anime.find(query)[0]["animeList"])
            if anime not in cur:
                cur.append(anime)
                newval = { "$set": { "animeList": cur}}
                self.anime.update_one(query,newval)
                await ctx.send(f"{anime} has been added to your list!")
            else:
                await ctx.send(f"{anime} is already on your list!")
        else:
            newval = { "_id": ctx.author.id, "animeList": list([anime])}
            self.anime.insert_one(newval)
            await ctx.send(f"{anime} has been added to your new list!")

    

    @commands.command()
    async def list_anime(self,ctx):
        query = {"_id": ctx.author.id }
        count = self.anime.count_documents(query)
        if count > 0:
            cur = self.anime.find(query)[0]
            string = ""
            anim = cur["animeList"]
            for i in range(len(anim)):
                string += f"**[{i}]**: {anim[i]}\n"
        
            embed = discord.Embed(title=f"{ctx.author.name} anime list", description= string)
            await ctx.send(embed=embed)




    

def setup(client):
    client.add_cog(AnimeNotify(client))