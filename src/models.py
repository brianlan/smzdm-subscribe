from mongoengine import IntField, StringField, BooleanField, ListField, DateTimeField
from mongoengine import connect, Document, Q

from src.settings import auth

connect('smzdm', host=auth['mongodb']['host'], port=auth['mongodb']['port'],
        username=auth['mongodb']['username'], password=auth['mongodb']['password'])


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
    row_cre_ts = DateTimeField()
    last_upd_ts = DateTimeField()

    def __repr__(self):
        return '[{}: {}] {}. (good: {}, bad: {})'.format(self.article_id, self.item_type, self.title, self.good_count,
                                                         self.bad_count)

    def __str__(self):
        return self.__repr__()

    def to_html(self):
        return '[{}] <a href={}>{}</a>. (good: {}, bad: {})'.format(self.item_type, self.detail_link, self.title,
                                                                    self.good_count, self.bad_count)


class Keyword(Document):
    keyword = StringField()

    @staticmethod
    def generate_mongoengine_queries():
        all_keywords = Keyword.objects.all()
        keyword_queries = Q(title__icontains='##@@?? Nothing_will_be_matched ##@@??')
        for kw in all_keywords:
            keyword_queries = keyword_queries | Q(title__icontains=kw.keyword)

        return keyword_queries
