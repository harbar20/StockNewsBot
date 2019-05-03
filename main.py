"""
StockNewsBot - a bot that gives stock & business news.
"""

#import all required modules
import discord
from discord.ext import commands
from newsapi import NewsApiClient

#initializing NewsAPI
newsAPI = NewsApiClient(api_key="84fc07b218c946beadd4ff6b81bc470a")

#creating the bot
client = commands.Bot(command_prefix="s!")

#when the bot goes online
@client.event
async def on_ready():
    print("StockNewsBot is online!")

