import os

from .abstract_communicator import AbstractCommunicator
from src.utils.logger_utils import get_logger

# ロガーの設定
logger = get_logger(__name__)

TEST_DATA = os.path.abspath("../../tests/data")


class TestCommunicator(AbstractCommunicator):
    def __init__(self):
        super(TestCommunicator, self).__init__()
        self.is_accessable = True
        self.is_communicatable = True
        self.is_loginable = True

    def validate_communicator(self):
        if not self.check_access():
            raise ValueError("{}のポートにアクセスする事が出来ませんでした。".format(self.device))
        if not self.check_communication():
            raise ValueError("{}に通信する事が出来ませんでした。".format(self.device))
        if not self.check_login():
            raise ValueError("{}にログインする事が出来ませんでした。".format(self.device))

    def check_access(self):
        return self.is_accessable

    def check_communication(self):
        return self.is_communicatable

    def check_login(self):
        return self.is_loginable

    def login(self, session):
        pass

    def admin_login(self, session):
        pass

    def communicate(self, command):
        f = open(os.path.join(TEST_DATA, "{}.log".format("_".join(command.split(" ")))), "r")
        return f.read()

    def logout(self, session):
        pass
