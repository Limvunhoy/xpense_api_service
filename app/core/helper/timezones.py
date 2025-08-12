from datetime import datetime, timezone, timedelta

UTC_PLUS_7 = timezone(timedelta(hours=7))

def get_now_utc_plus_7(): 
    return datetime.now(UTC_PLUS_7)