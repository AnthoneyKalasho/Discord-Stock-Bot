#!/usr/bin/env python3

from datetime import datetime


def is_market_open() -> bool:
    """
    Does some quick mafs to check if the stonk market is open
    :return: bool
    """
    now = datetime.now()
    return (now.weekday() < 5) and (5 <= (now.hour + (now.minute / 60)) <= 14)


def is_pre_market() -> bool:
    """
    Does some quick mafs to check if it's pre-market time
    :return: bool
    """
    now = datetime.now()
    return 5 <= (now.hour + (now.minute / 60)) <= 6.5


def is_after_hours() -> bool:
    """
    Does some quick mafs to check if it's after-hours gambling time
    :return: bool
    """
    now = datetime.now()
    return 13 <= (now.hour + (now.minute / 60)) <= 14


def should_parse_message(matches_len: int) -> bool:
    """
    Determines if a discord message should be parsed. We only
    parse up to and including 5 symbols per message
    :param matches_len: length of re.findall() resultant list
    :return: bool
    """

    return 0 < matches_len < 6
