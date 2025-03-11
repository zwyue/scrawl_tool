import time
from log import init_log
import shanbay_famous_sayings
import sched
import fund.scratch_fund

class Task:
    logger = init_log.logger

    s = sched.scheduler(time.time, time.sleep)

    def __init__(self):
        init_log.init(self)

    def execute_shanby_task(self):
        Shanbay = shanbay_famous_sayings.Shanbay(logger = self.logger)
        Shanbay.open()
        Shanbay.set_account()
        Shanbay.login()
        Shanbay.crack()
        time.sleep(5)

    def execute_fund_task(self):
        fund.scratch_fund.Fund(logger = self.logger).execute()

if __name__ == '__main__':
    task = Task()
    task.execute_shanby_task()
    task.execute_fund_task()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(task.execute_fund_task(), "cron",day_of_week = "0-4", hour = 14, minute = 30)
    # scheduler.add_job(task.execute_shanby_task(), "cron",hour = 11, minute = 30)
    # scheduler.start()