import logging, time
import os

cur_path = os.path.dirname(os.path.realpath(__file__))

log_path = os.path.join(os.path.dirname(cur_path), "logs")

if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log():
    def __init__(self):
        # 文件命名
        self.logname = os.path.join(log_path, f"{time.strftime('%Y_%m_%d_%H_%M_%S')}")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # 日志输出格式
        self.formater = logging.Formatter('[%(asctime)s] -%(filename)s] -%(levelname)s: %(message)s')

    def _console(self, level, message):
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formater)
        self.logger.addHandler(fh)
        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formater)
        self.logger.addHandler(ch)
        if level == 'info':
            self.logger.info(message)
        elif level =='debug':
            self.logger.debug(message)
        elif level=='warning':
            self.logger.warning(message)
        elif level=='error':
            self.logger.error(message)

        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)

        fh.close()
    def info(self,message):
        self._console("info",message)
    def debug(self,message):
        self._console('debug',message)

    def warning(self,message):
        self._console("warning",message)

    def error(self,message):
        self._console("error",message)
    def logger_info(self,func):
        def wrapper(*args,**kwargs):
            print(f"开始执行测试{func.__name}")
            func(*args,**kwargs)
            print(f"{func.__name}执行完毕")


if __name__ == '__main__':
    log=Log()
    log.info("__测试开始__")
    log.warning("__测试结束__")

