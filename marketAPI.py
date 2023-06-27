#!/usr/bin/env python3

import discord
import requests
from datetime import datetime
import json
import os
import utils

iexToken = os.environ['IEX_TOKEN']
fmpToken = os.environ['FMP_TOKEN']

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def get_basic_quote(ticker: str) -> discord.Embed:
    """
    Returns a discord.Embed object with basic quote info.
    :param ticker: stock ticker string (e.g. '$spy')
    :return: discord.Embed object containing message to be sent back to server 
    """

    page = requests.get('https://cloud.iexapis.com/stable/stock/' + ticker.replace('+','').replace('$','') + '/quote?token=' + iexToken)


    try:
        json_string = json.loads(page.text)
    except json.decoder.JSONDecodeError:
        print("Invalid or empty JSON received from IEX API")
        return None
    
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

def get_basic_quote_fmp(ticker: str) -> discord.Embed:

    url = 'https://financialmodelingprep.com/api/v3/quote/' + ticker + '?apikey=' + fmpToken


    try:
        json_string = get_jsonparsed_data(url)[0]
    except json.decoder.JSONDecodeError:
        print("Invalid or empty JSON received from IEX API")
        return None
    
    symbol = json_string["symbol"]
    companyName = json_string["name"]
    marketPercent = round(json_string["changesPercentage"], 3)
    latestPrice = json_string["price"]
    change = round(json_string["change"], 3)
    extendedHours = False

    now = datetime.now()
    if (5 <= (now.hour + (now.minute / 60)) <= 6.5) or (13 <= (now.hour + (now.minute / 60)) <= 14):
        extendedPrice = json_string["price"]
        extendedChange = json_string["change"]
        extendedChangePercent = round(json_string["changesPercentage"] * 100, 3)
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

