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
