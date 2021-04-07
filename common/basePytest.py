
from common.logger import Log

class Test_Pytest():
    def setup_class(self):
        # print("初始化")
        self.log=Log()
        self.log.info("初始化")

    def teardown_class(self):
        # print('清除')
        self.log.info("清除")

