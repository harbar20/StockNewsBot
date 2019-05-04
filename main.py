"""
StockNewsBot - a bot that gives stock & business news.
"""

#import all required modules
import discord
from discord.ext import commands
import requests
import xmltodict
import json
import asyncio

#creating the bot
bot = commands.Bot(command_prefix="s!")

#when the bot goes online
@bot.event
async def on_ready():
    loop = asyncio.get_event_loop()
    loop.create_task(sendArticle())
    
    print("StockNewsBot is online!")
    await bot.change_presence(activity=discord.Game(name="MarketWatch"))

#reads the code in the RSS feed and converts it to a dictionary
def xmlToDict(link):
    #given an XML link, it converts it to a dictionary
    
    #making a get request to the link
    xmlCode = requests.get(link)
    #converting code to a dictionary
    return xmltodict.parse(xmlCode.content)

#calls the articles json file
async def sendArticle():
    guild = bot.get_guild(565972212700676116)
    channel = discord.utils.get(guild.channels, name='general')

    while True:
        #writes the latest RSS feed to the json file
        with open("whatever.json", 'w') as f:
            json.dump(xmlToDict("https://www.google.com/alerts/feeds/17847585705873020513/17049360293039209726"), f)
    
        #reads the file
        with open("whatever.json") as f2:
            niceFile = json.load(f2)
            articles = niceFile["feed"]["entry"]
        #reads usedArticles file
        with open("usedArticles.json") as f3:
            usedArticles = json.load(f3)

        #sends the message
        i = 1
        for article in articles:
            if article not in usedArticles:
                usedArticles.append(article)
                await channel.send(article['link']['@href'])
            i+=1
    
        #rewrites usedArticles
        with open("usedArticles.json", 'w') as j:
            json.dump(usedArticles, j, indent=4)

        await asyncio.sleep(60*30)

bot.run("NTc0MDQ3NDk4MzAyMjU5MjAx.XMztaQ.3SKXpsTCwHeKq4dpP6jQmkduy3M")
