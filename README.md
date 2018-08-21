# Discord-Stock-Bot

To use simply write a stock ticker in chat like such "$TSLA". Also supports multiple tickers in 1 message "$TSLA $FDs"

Example Output:

![OutputImage.png](https://i.imgur.com/bH4G98X.png)

Currently supports stock quotes during regular trading hours.

[Data provided by IEXTrading](https://iextrading.com/developer/docs/#quote)

Planned Additions:
- Extended hours quotes
- Futures data
- Forex data

For the time being development is halted, but if you'd like to contribute, make a pull request and I'll push it through

# Instructions

1. [Install any version of Python 3](https://www.python.org/downloads/)
2. Install following dependencies:
  - [Discord API Python wrapper (Rewrite verison)](https://stackoverflow.com/questions/50686388/how-to-install-discord-py-rewrite)
  - [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) (pip install beautifulsoup4)
  - [Requests](http://docs.python-requests.org/en/master/) (pip install requests)
3. [Create a bot profile through Discord developer portal](https://discordapp.com/developers/applications/)
4. Generate a token on the "Bot" page and input it for the TOKEN variable in stockBot.py
5. Run stockBot.py
6. (Additional) [Invite bot to your server](https://github.com/jagrosh/MusicBot/wiki/Adding-Your-Bot-To-Your-Server)
