from urllib import request
from bs4 import BeautifulSoup

from models import Item


def text_strip(text):
    return text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')


url = 'http://www.smzdm.com/p1'
header = {'Host': 'www.smzdm.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Encoding': 'deflate',
          'Connection': 'keep-alive'}

req = request.Request(url, headers=header)
con = request.urlopen(req, timeout=1)
html = con.read()
con.close()
soup = BeautifulSoup(html)
soup.prettify()
items = soup.html.body.find_all('div', {'class': 'list '})

for item in items:
    new_item = Item(
        article_id=item.get('articleid'),
        region=item.div.a.get_text(),
        title=text_strip(item.div.h4.a.get_text()),
        tags=[text_strip(l.get_text()) for l in item.find('div', {'class': 'lrTop'}).find_all('a')],
        desc=item.find('div', {'class': 'lrInfo'}).get_text(),
        good_count=item.find('a', {'class': 'good'}).span.em.get_text(),
        bad_count=item.find('a', {'class': 'bad'}).span.em.get_text(),
        link=item.find('div', {'class': 'buy'}).a.get('href'),
    )
    new_item.save()
    print(new_item)
