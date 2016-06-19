from urllib import request
import datetime

from bs4 import BeautifulSoup
from mongoengine import Q
from mongoengine import DoesNotExist
from apscheduler.schedulers.blocking import BlockingScheduler

from models import Item, Keyword
from message_mail import sendmail
from settings import PAGES_IN_ONE_RUN, FIXED_HEADER, URL_PATTERN, logger, get_cur_ts, APS_SETTINGS, LOADING_JOB_ID


def text_strip(text):
    return text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')


def load_data():
    logger.info('Start loading data..')
    for page_num in range(1):
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
                try:
                    article_id = item.get('articleid')
                    has_good_bad = item.find('a', {'class': 'good'})

                    try:
                        db_item = Item.objects.get(article_id=article_id)
                        db_item.good_count = -1 if has_good_bad is None else item.find('a', {'class': 'good'}).span.em.get_text()
                        db_item.bad_count = -1 if has_good_bad is None else item.find('a', {'class': 'bad'}).span.em.get_text()
                        db_item.last_upd_ts = get_cur_ts()

                    except DoesNotExist:
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
                            last_upd_ts=get_cur_ts()
                        )

                    db_item.save()
                    logger.info('successfully inserted / updated {}'.format(db_item))

                except Exception as e:
                    logger.error(
                        'Error when creating / saving item (articleid={}). err_msg: {}'.format(item.get('articleid'), e))

    keyword_match_push()


def keyword_match_push():
    logger.info('Start keyword_match_push..')

    logger.info('Fetching predefined keyword list..')
    try:
        keyword_queries = Keyword.generate_mongoengine_queries()
    except Exception as e:
        logger.error('Error when querying keywords pre stored in DB. err_msg: {}'.format(e))
    else:
        try:
            keyword_matched_items = Item.objects.filter(
                Q(row_cre_ts__gt=get_cur_ts() - datetime.timedelta(days=1)) &
                Q(is_notified_keyword=False) &
                keyword_queries
            )
        except Exception as e:
            logger.error('Error when querying keyword match items. err_msg: {}'.format(e))

        if len(keyword_matched_items) > 0:
            try:
                subject = 'Subscribed SMZDM Items: {}'.format(keyword_matched_items[0].title)
                body = '<br>'.join([i.to_html() for i in keyword_matched_items])
                sendmail(subject, 'rlan@paypalcorp.com', ['rlan@paypalcorp.com'], body)
                logger.info('Mail has been pushed to receivers.')
            except Exception as e:
                logger.error('Error when pushing email. err_msg: {}'.format(e))
            else:
                for i in keyword_matched_items:
                    i.is_notified_keyword = True
                    i.save()


if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler(APS_SETTINGS['daemon'])
        scheduler.add_job(load_data, 'interval', misfire_grace_time=10, seconds=300, replace_existing=True,
                          id=LOADING_JOB_ID)
        scheduler.start()
    except (SystemExit, KeyboardInterrupt):
        logger.info('Exit signal triggered by user.')
        scheduler.shutdown()
