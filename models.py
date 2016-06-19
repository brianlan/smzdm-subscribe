import datetime

from pytz import timezone as tz
from mongoengine import connect, Document
from mongoengine import IntField, StringField, ListField, DateTimeField

from settings import MONGODB_SETTINGS, TIMEZONE


connect('smzdm', host=MONGODB_SETTINGS['host'])


class Item(Document):
    article_id = StringField(primary_key=True)
    region = StringField()
    title = StringField()
    tags = ListField()
    desc = StringField()
    good_count = IntField()
    bad_count = IntField()
    link = StringField()
    last_upd_ts = DateTimeField(default=datetime.datetime.now(tz(TIMEZONE)))

    def __repr__(self):
        return '[{}: {}] {}. (good: {}, bad: {})'.format(self.article_id, self.region, self.title, self.good_count,
                                                         self.bad_count)

    def __str__(self):
        return self.__repr__()