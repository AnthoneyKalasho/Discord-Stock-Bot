import discord
from discord.ext import commands
import utils
import re
import requests
import json
from datetime import datetime
import os

TOKEN = os.environ['TOKEN']
#TOKEN = "YOUR TOKEN HERE"
client = discord.Client()
pattern_quote = re.compile(r'\$([^\s]+)')
pattern_chart = re.compile(r'&chart +([A-Z]+)')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with Stonks"))


@client.event
async def on_message(message: discord.message.Message):
    if message.author.id != client.user.id:  # fix recursive spam
        if utils.is_market_open():
            for m in re.findall(pattern_quote, message.content):
                if(len(m) > 5 or not m.isalpha()):
                    return
                else:
                    page = requests.get('https://api.iextrading.com/1.0/stock/'
                                        + m + '/quote')
                    json_string = json.loads(page.text)
                    symbol = json_string["symbol"]
                    companyName = json_string["companyName"]
                    marketPercent = round(json_string["changePercent"] * 100, 3)
                    latestPrice = json_string["latestPrice"]
                    change = round(json_string["change"], 3)
                    extendedHours = False

                    now = datetime.now()
                    if (5 <= (now.hour + (now.minute/60)) <= 6.5) or (13 <= (now.hour + (now.minute/60)) <= 14):
                        extendedPrice = json_string["extendedPrice"]
                        extendedChange = json_string["extendedChange"]
                        extendedChangePercent = round(json_string["extendedChangePercent"] * 100, 3)
                        if extendedChangePercent >= 0:
                            positive = "+"
                        else:
                            positive = ""

                    if utils.is_pre_market():
                        marketTime = "PM"
                        extendedHours = True
                    elif utils.is_after_hours():
                        marketTime = "AH"
                        extendedHours = True

                    if marketPercent >= 0:
                        marketPercentString = "+" + str(marketPercent) + "%"
                    else:
                        marketPercentString = str(marketPercent) + "%"

                    if change >= 0:
                        changeString = "+" + str(change)
                    else:
                        changeString = str(change)

                    if extendedHours:
                        embed = discord.Embed(title="" + companyName +
                                              " ($" + symbol + ")",
                                              url="https://www.tradingview.com/symbols/"
                                              + symbol,
                                              description=str(round(latestPrice, 3))
                                              + " -> (" + changeString
                                              + " / " + marketPercentString
                                              + ")" + " | "
                                              + marketTime + " "
                                              + str(round(extendedPrice, 3))
                                              + " -> (" + positive
                                              + str(extendedChange)
                                              + " / " + positive + str(round(extendedChangePercent, 2)) + "%"
                                              + ")", color=0x006BB6)
                    else:
                        embed = discord.Embed(title=""
                                              + companyName
                                              + " ($" + symbol + ")",
                                              url="https://www.tradingview.com/symbols/"
                                              + symbol,
                                              description=str(round(latestPrice, 3)) +
                                              " -> (" + changeString
                                              + " / " + marketPercentString
                                              + ")", color=0x006BB6)
                    await message.channel.send(embed=embed)

        else:
            if re.match(pattern_quote, message.content):
                await message.channel.send("Market is closed ya retard. Go do something else.")


@client.event
async def on_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument: {}".format(error.param))

client.run(TOKEN)
