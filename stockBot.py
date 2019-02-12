#!/usr/bin/env python3

import discord
from discord.ext import commands
import utils
import marketAPI as api
import re
import os

TOKEN = os.environ['TOKEN']
#TOKEN = "YOUR TOKEN HERE"
client = commands.Bot(command_prefix='!')
pattern_quote = re.compile(r'[$]([A-Za-z]+)[+]?')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with Stonks"))

@client.command()
async def halted(ctx, ticker):
    await ctx.send(embed=api.get_halt_status(ticker))

@client.event
async def on_message(message: discord.message.Message):
    if message.author.id != client.user.id:  # fix recursive spam
        matches = re.findall(pattern_quote, message.content)
        matches_len = len(matches)

        if utils.should_parse_message(matches_len):
            for m in matches:
                if m[-1] == '+':
                    embed = api.get_extended_quote(m)
                    await message.channel.send(embed=embed)
                else:
                    embed = api.get_basic_quote(m)
                    await message.channel.send(embed=embed)

        else:
            if matches_len > 0:
                await message.channel.send("Market is closed ya retard. Go do something else.")
            else:
                await client.process_commands(message)


@client.event
async def on_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument: {}".format(error.param))

client.run(TOKEN)
