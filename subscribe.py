from urllib import request

from bs4 import BeautifulSoup

from models import Item
from settings import PAGES_IN_ONE_RUN, FIXED_HEADER, URL_PATTERN, logger, get_cur_ts, INFO_TYPES


def text_strip(text):
    return text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')


def load_data():
    for page_num in range(PAGES_IN_ONE_RUN):
        url = URL_PATTERN.format(page_num=page_num+1)
        req = request.Request(url, headers=FIXED_HEADER)
        try:
            con = request.urlopen(req, timeout=5)
        except Exception as e:
            logger.error('Error when trying to connect {} using urllib.request. err_msg: {}'.format(url, e))
        else:
            html = con.read()
            con.close()
            soup = BeautifulSoup(html)
            soup.prettify()
            items = soup.html.body.find_all('div', {'class': 'list '})

            for item in items:
                item_type = item.div.a.get_text()
                new_item = Item(
                    article_id=item.get('articleid'),
                    item_type=item_type,
                    title=text_strip(item.div.h4.a.get_text()),
                    detail_link=item.div.h4.a.get('href'),
                    tags=[text_strip(l.get_text()) for l in item.find('div', {'class': 'lrTop'}).find_all('a')],
                    desc=item.find('div', {'class': 'lrInfo'}).get_text(),
                    good_count=-1 if item_type in INFO_TYPES else item.find('a', {'class': 'good'}).span.em.get_text(),
                    bad_count=-1 if item_type in INFO_TYPES else item.find('a', {'class': 'bad'}).span.em.get_text(),
                    item_direct_link='' if item_type in INFO_TYPES else item.find('div', {'class': 'buy'}).a.get('href'),
                    last_upd_ts=get_cur_ts()
                )
                new_item.save()
                print(url, new_item)


if __name__ == '__main__':
    load_data()
