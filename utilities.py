import datetime
from pytz import timezone as tz
from settings import TIMEZONE


def text_strip(text):
    return text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')


def get_cur_ts():
    return datetime.datetime.now(tz(TIMEZONE))
