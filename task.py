import sched
import time

from apscheduler.schedulers.blocking import BlockingScheduler

import fund.scratch_fund
import shanbay_famous_sayings
from log import init_log


class Task:
    logger = init_log.logger

    s = sched.scheduler(time.time, time.sleep)

    def __init__(self):
        init_log.init(self)

    def execute_shanby_task(self):
        Shanbay = shanbay_famous_sayings.Shanbay(logger=self.logger)
        Shanbay.open()
        Shanbay.set_account()
        Shanbay.login()
        Shanbay.crack()
        time.sleep(5)

    def execute_fund_task(self):
        fund.scratch_fund.Fund(logger=self.logger, locate="account.json").execute()


if __name__ == '__main__':
    task = Task()
    scheduler = BlockingScheduler()
    scheduler.add_job(task.execute_fund_task, 'cron', day_of_week='mon-fri', hour='9-15', minute='*/20')
    scheduler.add_job(task.execute_shanby_task, "cron", hour=10, minute=50)
    scheduler.start()
