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

#getting the token
with open("config.json") as c:
    config = json.load(c)
    token = config["token"]

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

def articleEmbed(headline, link, upDate):
    #creating the actual embed
    articleEmbed = discord.Embed(
        title = headline,
        description = link,
        colour = discord.Colour.green()
    )

    #adding extra details to the embed
    articleEmbed.add_field(name="Last Updated", value=upDate)

    return articleEmbed

#calls the articles json file
async def sendArticle():
    guild = bot.get_guild(434323921303633930)
    channel = discord.utils.get(guild.channels, name='newsbot')

    while True:
        #writes the latest RSS feed to the json file
        with open("whatever.json", 'w') as f:
            json.dump(xmlToDict("https://seekingalpha.com/market_currents.xml"), f)
    
        #reads the file
        with open("whatever.json") as f2:
            niceFile = json.load(f2)
            articles = niceFile["rss"]["channel"]["item"]
        #reads usedArticles file
        with open("usedArticles.json") as f3:
            usedArticles = json.load(f3)

        #sends the message
        i = 0
        for article in articles:
            if article not in usedArticles:
                usedArticles.append(article)

                #setting variables for the embed
                headline = article["title"]
                link = article['link']
                upDate = article["pubDate"]

                #sending the embed
                await channel.send(embed=articleEmbed(headline, link, upDate))
            i+=1
    
        #rewrites usedArticles
        with open("usedArticles.json", 'w') as j:
            json.dump(usedArticles, j, indent=4)

        await asyncio.sleep(60*30)

bot.run(token)
