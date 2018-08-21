import discord
import re
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, time, date

TOKEN = 'INSERT TOKEN HERE'

client = discord.Client()
pattern = re.compile(r'\$([^\s]+)')

@client.event
async def on_message(message):
    nowTime = datetime.now()

    thisHour = nowTime.hour
    #ONLY TAKES COMMANDS BETWEEN 6AM and 2PM PST, EDIT TO YOUR TIMEZONE
    if (nowTime.weekday() < 5) and (6 <= thisHour <= 14):
        if message.author == client.user:
            return
        for m in re.findall(pattern, message.content):
            if(len(m)>5 or not m.isalpha()):
                return
            else:
                page = requests.get('https://api.iextrading.com/1.0/stock/'+m+'/quote')
                json_string = json.loads(page.text)
                symbol = json_string["symbol"]
                companyName = json_string["companyName"]
                marketPercent = round(json_string["changePercent"] * 100, 3)
                marketPercentString = str(marketPercent) + "%"
                if(marketPercent>=0):
                    marketPercentString = "+" + marketPercentString
                latestPrice = json_string["latestPrice"]
                change = round(json_string["change"],3)
                changeString=str(change)
                if(change>=0):
                    changeString = "+" + changeString
                embed = discord.Embed(title=""+companyName+" ($"+symbol + ")", url="https://www.tradingview.com/symbols/"+symbol,description=str(round(latestPrice,3)) + " -> ("+changeString+" / "+marketPercentString+")", color=0x006BB6)
                await message.channel.send(embed=embed)
    else:
        return

client.run(TOKEN)