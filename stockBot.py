#!/usr/bin/env python3

import discord
from discord.ext import commands
import utils
import marketAPI as api
import re
import os



TOKEN = os.environ['TOKEN']
pattern_quote = re.compile(r'[$]([A-Za-z]+)[+]?')

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        super().__init__(intents=intents) 

    async def on_ready(self):
        await client.change_presence(status=discord.Status.online, activity=discord.Game("with Stonks"))

    async def on_message(self, message: discord.message.Message):
        if message.author.id != client.user.id:  # fix recursive spam
            matches = re.findall(pattern_quote, message.content)
            matches_len = len(matches)

            if utils.should_parse_message(matches_len):
                for m in matches:
                    embed = api.get_basic_quote_fmp(m)
                    await message.channel.send(embed=embed)

            else:
                if matches_len > 0:
                    await message.channel.send("Market is closed. Go do something else")
                else:
                    pass

client = MyClient()
client.run(TOKEN)
