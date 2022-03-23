
import serial
import serial.tools.list_ports


from .abstract_communicator import AbstractCommunicator
from src.utils.logger_utils import get_logger

# ロガーの設定
logger = get_logger(__name__)


class SerialCommunicator(AbstractCommunicator):
    def __init__(self):
        super(SerialCommunicator, self).__init__()

    def validate_communicator(self):
        if not self.check_access():
            raise ValueError("{}のポートにアクセスする事が出来ませんでした。".format(self.device))
        if not self.check_communication():
            raise ValueError("{}に通信する事が出来ませんでした。".format(self.device))
        if not self.check_login():
            raise ValueError("{}にログインする事が出来ませんでした。".format(self.device))

    def check_access(self):
        for port in serial.tools.list_ports.comports():
            if port is self.device.port_name:
                return True
        return False

    def check_communication(self):
        with self.get_session() as session:
            result = self.command(session, "\r")

        if len(result) > 0:
            return True
        return False

    def check_login(self):
        with self.get_session() as session:
            result = self.login(session)

        if not result or self.determine_login(result):
            return True
        return False

    def login(self, session):
        login_result = ""
        session.write("\r".encode())
        enter_result = self.read_all(session)
        login_flag = self.determine_login(enter_result)
        admin_login_flag = self.determine_admin_login(enter_result)

        if not login_flag and not admin_login_flag:
            session.write("{}\r".format(self.device.login_password).encode())
            login_result = self.read_all(session)

        return login_result

    def admin_login(self, session):
        admin_login_result = ""
        session.write("\r".encode())
        enter_result = self.read_all(session)
        admin_login_flag = self.determine_admin_login(enter_result)

        if not admin_login_flag:
            session.write("enable\r".encode())
            session.write("{}\r".format(self.device.login_password).encode())
            admin_login_result = self.read_all(session)

        return admin_login_result

    def command(self, session, command: str) -> str:
        session.write("{}\r".format(command).encode())
        result = self.read_all(session)

        return result

    def logout(self, session):
        session.write("exit\r".encode())

    def communicate(self, command: str) -> str:
        # TODO commandはStringではなくCommandクラスで実行出来るようにする。
        with self.get_session() as session:
            self.login(session)
            self.admin_login(session)
            result = self.command(session, command)

        return result

    def get_session(self):
        return serial.Serial(port=self.device.port_name, baudrate=self.device.baudrate, timeout=1)

    @staticmethod
    def determine_login(result):
        # TODO 機器や機種によって異なるためリファクタ
        return ">" in result

    @staticmethod
    def determine_admin_login(result):
        # TODO 機器や機種によって異なるためリファクタ
        return "#" in result

    @staticmethod
    def read_all(session) -> str:
        result = ""
        while True:
            log = session.read().decode()

            if not len(log) and not session.in_waiting:
                return result

            result += log


if __name__ == '__main__':
    com = SerialCommunicator()

    print("communicatable   : {}".format(com.check_communication()))
    print("loginable        : {}".format(com.check_login()))
    print("result           : {}".format(com.communicate("show run")))
