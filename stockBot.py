#!/usr/bin/env python3

import discord
from discord.ext import commands
import utils
import marketAPI as api
import re
import os

TOKEN = os.environ['TOKEN']
#TOKEN = "YOUR TOKEN HERE"
client = discord.Client()
pattern_quote = re.compile(r'\$([^\s]+)')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with Stonks"))


@client.event
async def on_message(message: discord.message.Message):
    if message.author.id != client.user.id:  # fix recursive spam
        matches = re.findall(pattern_quote, message.content)
        matches_len = len(matches)

        if utils.should_parse_message(matches_len):
            for m in matches:
                if not m.isalpha():
                    return
                else:
                    embed = api.get_basic_quote(m)
                    await message.channel.send(embed=embed)

        else:
            if matches_len > 0:
                await message.channel.send("Market is closed ya retard. Go do something else.")


@client.event
async def on_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument: {}".format(error.param))

client.run(TOKEN)
