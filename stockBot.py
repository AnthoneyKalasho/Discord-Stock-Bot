import discord
import re
import requests
import json
from datetime import datetime, time, date
import os

TOKEN = os.environ['TOKEN']
#TOKEN = "COMMENT OUT ABOVE LINE AND PUT YOUR TOKEN HERE"
client = discord.Client()
pattern = re.compile(r'\$([^\s]+)')


@client.event
async def on_message(message):
    now = datetime.now()
    if (now.weekday() < 5) and (5 <= (now.hour + (now.minute/60)) <= 14):
        if message.author == client.user:
            return
        for m in re.findall(pattern, message.content):
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

                if (5 <= (now.hour + (now.minute/60)) <= 6.5) or (13 <= (now.hour + (now.minute/60)) <= 14):
                    extendedPrice = json_string["extendedPrice"]
                    extendedChange = json_string["extendedChange"]
                    extendedChangePercent = round(json_string["extendedChangePercent"] * 100, 3)
                    if extendedChangePercent >= 0:
                        positive = "+"
                    else:
                        positive = ""

                if (5 <= (now.hour + (now.minute/60)) <= 6.5):
                    marketTime = "PM"
                    extendedHours = True
                elif (13 <= (now.hour + (now.minute/60)) <= 14):
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

client.run(TOKEN)
