import logging
import time
import os

logger = logging.getLogger()

def init(self,locate='./Logs\\'):
    # Log等级总开关
    self.logger.setLevel(logging.INFO)
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    log_path = mkdir(locate)
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w', encoding="UTF-8")
    # 输出到file的log等级的开关
    fh.setLevel(logging.INFO)
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    self.logger.addHandler(fh)

    # # 日志打印到屏幕上
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    self.logger.addHandler(ch)

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    return path