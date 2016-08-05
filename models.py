class Item(object):
    def __init__(self, article_id, item_type, title, detail_link, tags, desc, good_count, bad_count, item_direct_link,
                 row_cre_ts, last_upd_ts, is_notified_keyword=False):
        self.article_id = article_id
        self.item_type = item_type
        self.title = title
        self.detail_link = detail_link
        self.tags = tags
        self.desc = desc
        self.good_count = good_count
        self.bad_count = bad_count
        self.item_direct_link = item_direct_link
        self.is_notified_keyword = is_notified_keyword
        self.row_cre_ts = row_cre_ts
        self.last_upd_ts = last_upd_ts

    def __repr__(self):
        return '[{}: {}] {}. (good: {}, bad: {})'.format(self.article_id, self.item_type, self.title, self.good_count,
                                                         self.bad_count)

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        doc = {
            '_id': self.article_id,
            'item_type': self.item_type,
            'title': self.title,
            'detail_link': self.detail_link,
            'tags': self.tags,
            'desc': self.desc,
            'good_count': self.good_count,
            'bad_count': self.bad_count,
            'item_direct_link': self.item_direct_link,
            'is_notified_keyword': self.is_notified_keyword,
            'row_cre_ts': self.row_cre_ts,
            'last_upd_ts': self.last_upd_ts,
        }
        return doc

    def to_html(self):
        return '[{}] <a href={}>{}</a>. (good: {}, bad: {})'.format(self.item_type, self.detail_link, self.title,
                                                                    self.good_count, self.bad_count)


class Keyword(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def to_dict(self):
        return {'keyword': self.keyword}
