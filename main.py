from apscheduler.schedulers.blocking import BlockingScheduler

from src.subscribe import load_data
from src.settings import APS_SETTINGS, LOADING_JOB_ID, logger


if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler(APS_SETTINGS['daemon'])
        scheduler.add_job(load_data, 'interval', misfire_grace_time=10, seconds=300, replace_existing=True,
                          id=LOADING_JOB_ID)
        scheduler.start()
    except (SystemExit, KeyboardInterrupt):
        logger.info('Exit signal triggered by user.')
        scheduler.shutdown()
