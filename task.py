import argparse
import os
import sched
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

import fund.scratch_fund
import shanbay_famous_sayings
from log import init_log


class Task:
    logger = init_log.logger

    s = sched.scheduler(time.time, time.sleep)

    def __init__(self):
        init_log.init(self, locate=os.environ.get("LOG_PATH"))

    def execute_shanby_task(self):
        shanbay = shanbay_famous_sayings.Shanbay(logger=self.logger, user_data_dir=os.environ.get("CHROME_USER_DATA_DIR"))
        shanbay.open(file=os.environ.get("ACCOUNT_PATH"))
        shanbay.set_account()
        shanbay.login()
        shanbay.crack()
        shanbay.driver.quit()

    def execute_fund_task(self):
        fund.scratch_fund.Fund(logger=self.logger).execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default=os.environ.get("ENV_FILE"))
    args = parser.parse_args()
    load_dotenv(args.env)

    env = os.environ.get("ENV")

    task = Task()
    if env == 'dev':
        task.execute_fund_task()
        task.execute_shanby_task()

    if env == 'prod':
        scheduler = BlockingScheduler()
        scheduler.add_job(task.execute_shanby_task, "cron", hour=13, minute=10)
        scheduler.add_job(task.execute_fund_task, 'cron', day_of_week='mon-fri', hour='10-11', minute='*/28')
        scheduler.add_job(task.execute_fund_task, 'cron', day_of_week='mon-fri', hour='14-15', minute='*/28')
        scheduler.start()
