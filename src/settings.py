import os
import logging
import datetime

import yaml
from pytz import timezone as tz
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore


LOG_DIR = 'log'

TIMEZONE = 'Asia/Shanghai'

with open('auth.yml', 'r') as f:
    auth = yaml.load(f)

PAGES_IN_ONE_RUN = 30

URL_PATTERN = 'http://www.smzdm.com/jingxuan/p{page_num}'

FIXED_HEADER = {'Host': 'www.smzdm.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'deflate',
                'Connection': 'keep-alive'}

DEFAULT_SENDER = 'rongyilan@126.com'
DEFAULT_RECEIVERS = ['lanrongyi@motovis.com']

# Apscheduler Settings
LOADING_JOB_ID = '100166'

APS_SETTINGS = {
    'daemon': {
        'jobstores': {
            'default': MemoryJobStore(),
        },

        'executors': {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        },

        'job_defaults': {
            'coalesce': True,
            'max_instances': 1
        }
    },
}

config = {
    'mongodb': {
        'host': 'mongodb',
        'port': 27017
    }
}


# Define Logger
def get_cur_ts():
    return datetime.datetime.now(tz(TIMEZONE))


logger = logging.getLogger('smzdm-subscribe')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.sep.join([
    LOG_DIR,
    datetime.datetime.strftime(get_cur_ts(), '%Y%m%d')
]))
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
