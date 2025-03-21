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
        Shanbay = shanbay_famous_sayings.Shanbay(logger=self.logger, userDataDir=os.environ.get("CHROME_USER_DATA_DIR"))
        Shanbay.open(file=os.environ.get("ACCOUNT_PATH"))
        Shanbay.set_account()
        Shanbay.login()
        Shanbay.crack()
        time.sleep(5)

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
        task.execute_shanby_task()
        task.execute_fund_task()

    if env == 'prod':
        scheduler = BlockingScheduler()
        scheduler.add_job(task.execute_shanby_task, "cron", hour=13, minute=30)
        scheduler.add_job(task.execute_fund_task, 'cron', day_of_week='mon-fri', hour='11-15', minute='*/20')
        scheduler.start()
