from log import init_log


class Train:
    # 创建一个logger
    logger = init_log.logger

    def __init__(self):
        init_log.init(self)