
import requests
import datetime
import pandas as pd
import re
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from tabulate import tabulate

url = 'https://www.worldometers.info/coronavirus/'

class HTMLTableParser():

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [(table['id'],self.parse_html_table(table))\
            for table in soup.find_all('table')]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []

        for row in table.find_all('tr'):
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    n_columns = len(td_tags)
        
        th_tags = row.find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())
        
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                    index = range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text().upper()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        
        return df

class Corona(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def cov(self,ctx,*, country):
        """ Get statistics for specified country about Corona Virus (Sars-Cov-2) """
        if country is not None:
            hp = HTMLTableParser()
            table = hp.parse_url(url)[0][1]
            t= table.loc[table[0] == country.upper()] 
            
            if len(t) > 0:
                
                embed=discord.Embed(title="Corona Virus", description=country.upper(), color=0xbde12b)
                pattern = r"\s"

                cases = re.split(pattern,t[1].to_string())[4]
                new_cases = re.split(pattern,t[2].to_string())[4]

                deaths = re.split(pattern,t[3].to_string())[4]
                new_deaths = re.split(pattern,t[4].to_string())[4]

                recovered = re.split(pattern,t[5].to_string())[4]

                embed.add_field(name="Current cases", value=f"{cases} {new_cases}", inline=True)
                embed.add_field(name="Recovered", value=recovered, inline=True)
                embed.add_field(name="Current deaths", value=f"{deaths} {new_deaths}", inline=True)
                embed.set_footer(text="Rimuru")

                await ctx.send(embed=embed)

            else:
                embed=discord.Embed(title="Corona Virus", color=0xbde12b)
                embed.add_field(name="This country does not exist or is not infected! ", value="You can get full list from [here](https://www.worldometers.info/coronavirus/)", inline=True)
                embed.set_footer(text="Rimuru")
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Corona(client))

