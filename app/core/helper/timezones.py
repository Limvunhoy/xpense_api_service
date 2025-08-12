from datetime import datetime, timezone, timedelta

UTC_PLUS_7 = timezone(timedelta(hours=7))


def get_now_utc_plus_7() -> datetime:
    """Returns current datetime in UTC+7 without timezone info"""
    return datetime.now() + timedelta(hours=7)
