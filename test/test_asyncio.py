import aiohttp
import asyncio
from bs4 import BeautifulSoup
import motor.motor_asyncio
from utilities import get_cur_ts, text_strip
from settings import FIXED_HEADER


client = motor.motor_asyncio.AsyncIOMotorClient('10.24.144.31', 27017)
db = client.smzdm_dev


class Item:
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

async def fetch_page(session, url):
    with aiohttp.Timeout(30):
        async with session.get(url, headers=FIXED_HEADER) as response:
            assert response.status == 200
            content = await response.read()
            await parse_items_in_one_page(content)


async def parse_item(item):
    try:
        article_id = item.get('articleid')
        has_good_bad = item.find('a', {'class': 'good'})

        db_item = Item(
            article_id=article_id,
            item_type=item.div.a.get_text(),
            title=text_strip(item.div.h4.a.get_text()),
            detail_link=item.div.h4.a.get('href'),
            tags=[text_strip(l.get_text()) for l in item.find('div', {'class': 'lrTop'}).find_all('a')],
            desc=item.find('div', {'class': 'lrInfo'}).get_text(),
            good_count=-1 if has_good_bad is None else item.find('a', {'class': 'good'}).span.em.get_text(),
            bad_count=-1 if has_good_bad is None else item.find('a', {'class': 'bad'}).span.em.get_text(),
            item_direct_link='' if has_good_bad is None else item.find('div', {'class': 'buy'}).a.get('href'),
            row_cre_ts=get_cur_ts(),
            last_upd_ts=get_cur_ts()
        )

        await db.item.insert(db_item.to_dict())
        print('successfully inserted / updated {}'.format(db_item))

    except Exception as e:
        print(
            'Error when creating / saving item (articleid={}). err_msg: {}'.format(item.get('articleid'), e))


async def parse_items_in_one_page(html):
    soup = BeautifulSoup(html)
    soup.prettify()
    items = soup.html.body.find_all('div', {'class': 'list '})

    for item in items:
        await parse_item(item)


def test_asyncio_get_html():
    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession(loop=loop) as session:
        tasks = [fetch_page(session, 'http://www.smzdm.com/p'+str(i)) for i in range(1, 31)]
        loop.run_until_complete(asyncio.wait(tasks))

    loop.close()

