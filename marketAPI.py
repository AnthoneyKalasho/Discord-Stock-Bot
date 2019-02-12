#!/usr/bin/env python3

import discord
import requests
from datetime import datetime
import json

import utils


def get_basic_quote(ticker: str) -> discord.Embed:
    """
    Returns a discord.Embed object with basic quote info.
    :param ticker: stock ticker string (e.g. '$spy')
    :return: discord.Embed object containing message to be sent back to server
    """

    page = requests.get('https://api.iextrading.com/1.0/stock/' + ticker.replace('+','').replace('$','') + '/quote')
    json_string = json.loads(page.text)
    symbol = json_string["symbol"]
    companyName = json_string["companyName"]
    marketPercent = round(json_string["changePercent"] * 100, 3)
    latestPrice = json_string["latestPrice"]
    change = round(json_string["change"], 3)
    extendedHours = False

    now = datetime.now()
    if (5 <= (now.hour + (now.minute / 60)) <= 6.5) or (13 <= (now.hour + (now.minute / 60)) <= 14):
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

    title = "".join([companyName, " ($", symbol, ")"])
    url = "https://www.tradingview.com/symbols/" + symbol
    description = "".join([str(round(latestPrice, 3)),
                           " -> (",
                           changeString,
                           " / ",
                           marketPercentString,
                           ")"])
    if extendedHours:
        description = "".join([str(round(latestPrice, 3)),
                               " -> (",
                               changeString,
                               " / ",
                               marketPercentString,
                               ")",
                               " | ",
                               marketTime,
                               " ",
                               str(round(extendedPrice, 3)),
                               " -> (",
                               positive,
                               str(extendedChange),
                               " / ",
                               positive,
                               str(round(extendedChangePercent, 2)),
                               "%",
                               ")"])

    return discord.Embed(title=title, url=url, description=description, color=0x006BB6)


def get_extended_quote(ticker: str) -> discord.Embed:
    """
    Returns a discord.Embed object with extended quote info.
    :param ticker: stock ticker string (e.g. '$spy+')
    :return: discord.Embed object containing message to be sent back to server
    """

    page = requests.get('https://api.iextrading.com/1.0/stock/' + ticker.replace('+','').replace('$','') + '/quote')
    json_string = json.loads(page.text)
    symbol = json_string["symbol"]
    companyName = json_string["companyName"]
    marketPercent = round(json_string["changePercent"] * 100, 3)
    latestPrice = json_string["latestPrice"]
    change = round(json_string["change"], 3)
    extendedHours = False

    now = datetime.now()
    if (5 <= (now.hour + (now.minute / 60)) <= 6.5) or (13 <= (now.hour + (now.minute / 60)) <= 14):
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

    title = "".join([companyName, " ($", symbol, ")"])
    url = "https://www.tradingview.com/symbols/" + symbol
    description = "".join([str(round(latestPrice, 3)),
                           " -> (",
                           changeString,
                           " / ",
                           marketPercentString,
                           ")"])
    if extendedHours:
        description = "".join([str(round(latestPrice, 3)),
                               " -> (",
                               changeString,
                               " / ",
                               marketPercentString,
                               ")",
                               " | ",
                               marketTime,
                               " ",
                               str(round(extendedPrice, 3)),
                               " -> (",
                               positive,
                               str(extendedChange),
                               " / ",
                               positive,
                               str(round(extendedChangePercent, 2)),
                               "%",
                               ")"])

    return discord.Embed(title=title, url=url, description=description, color=0x006BB6)

def get_halt_status(ticker: str) -> discord.Embed:
    """

    :param ticker: stock ticker string (e.g. 'spy')
    :return:
    """

    raw_data = requests.get('https://api.iextrading.com/1.0/deep/op-halt-status?symbols=' + ticker)
    json_string = json.loads(raw_data.text)[ticker.upper()]
    isHalted = json_string['isHalted']
    timestamp = datetime.utcfromtimestamp(1549943089).strftime('%Y-%m-%d %H:%M:%S')

    raw_data = requests.get('https://api.iextrading.com/1.0/stock/' + ticker + '/quote')
    json_string = json.loads(raw_data.text)
    symbol = json_string["symbol"]

    companyName = json_string["companyName"]
    title = "".join([companyName, " ($", symbol, ")"])
    url = "https://www.tradingview.com/symbols/" + symbol
    description = "Halted at %s".format(timestamp) if isHalted else "Not halted, so go buy some FDs."

    return discord.Embed(title=title, url=url, description=description)

