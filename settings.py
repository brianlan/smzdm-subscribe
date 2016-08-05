import os
import logging
import datetime
from pytz import timezone as tz

import yaml
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore


PROJECT_DIR = '/home/rlan/projects/smzdm-subscribe/smzdm-subscribe'
LOG_DIR = '/home/rlan/log'
# PROJECT_DIR = '/Users/rlan/Work/playground/smzdm-subscribe'
# LOG_DIR = '/tmp'

MAIL_SERVER = 'atom.paypalcorp.com'

TIMEZONE = 'Asia/Shanghai'

with open(os.path.join(PROJECT_DIR, 'config.yaml'), 'r') as f:
    config = yaml.load(f)

MONGODB_SETTINGS = config['MONGODB_SETTINGS']

PAGES_IN_ONE_RUN = 30

URL_PATTERN = 'http://www.smzdm.com/p{page_num}'

FIXED_HEADER = {'Host': 'www.smzdm.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'deflate',
                'Connection': 'keep-alive'}

DEFAULT_SENDER = 'rlan@paypalcorp.com'
DEFAULT_RECEIVERS = ['rlan@paypalcorp.com']

# Apscheduler Settings
LOADING_JOB_ID = '100166'

APS_SETTINGS = {
    'daemon': {
        'jobstores': {
            'default': MemoryJobStore(),
        },

        'executors': {
            'default': ThreadPoolExecutor(1),
            'processpool': ProcessPoolExecutor(1)
        },

        'job_defaults': {
            'coalesce': True,
            'max_instances': 1
        }
    },
}


# Define Logger
logger = logging.getLogger('smzdm-subscribe')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.sep.join([
    LOG_DIR,
    datetime.datetime.strftime(datetime.datetime.now(tz(TIMEZONE)), '%Y%m%d')
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
