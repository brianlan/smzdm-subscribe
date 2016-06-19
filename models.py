from mongoengine import connect, Document
from mongoengine import IntField, StringField, BooleanField, ListField, DateTimeField

from settings import MONGODB_SETTINGS, TIMEZONE, get_cur_ts


connect('smzdm', host=MONGODB_SETTINGS['host'])


class Item(Document):
    article_id = StringField(primary_key=True)
    item_type = StringField()
    title = StringField()
    detail_link = StringField()
    tags = ListField()
    desc = StringField()
    good_count = IntField()
    bad_count = IntField()
    item_direct_link = StringField()
    is_notified_keyword = BooleanField(default=False)
    row_cre_ts = DateTimeField(default=get_cur_ts())
    last_upd_ts = DateTimeField()

    def __repr__(self):
        return '[{}: {}] {}. (good: {}, bad: {})'.format(self.article_id, self.item_type, self.title, self.good_count,
                                                         self.bad_count)

    def __str__(self):
        return self.__repr__()

    def to_html(self):
        return '[{}] <a href={}>{}</a>. (good: {}, bad: {})'.format(self.item_type, self.detail_link, self.title,
                                                                    self.good_count, self.bad_count)
