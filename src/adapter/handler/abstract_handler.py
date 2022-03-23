from abc import ABC, abstractmethod
from enum import Enum
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
# from communicator.serial_communicator import SerialCommunicator
from communicator.test_communicator import TestCommunicator


class HandlerCommand(Enum):
    CHECK = "check"
    RUN = "run"


class AbstractHandler(ABC):
    REQUIRED_KEYS = ["cfile", "inventory", "command", "method"]

    def __init__(self, app):
        """
        :description
            AbstractHandlerクラスのイニシャライザ
        :param
            app : AbstractApp
        """
        self.app = app

    @staticmethod
    def check_file(file_path):
        """
        :description
            ファイルが存在するかチェックするスタティックメソッド
        :param
            file_path    : str   ファイルのパス
        :return          : bool  ファイルのパスが存在すればTrueとなり、それ以外はFalseとなる。
        """
        return os.path.isfile(file_path)

    def check_attribution(self, args):
        """
        :description
            辞書型の引数に特定のキーが含まれているか確認するインスタンスメソッド
        :param
            args    : dictionary    argparseで解析した結果
        :return     : bool          REQUIRED_KEYSが存在すればTrueとなり、それ以外はFalseとなる。
        """
        return all([attr in self.REQUIRED_KEYS for attr in args.__dict__.keys()])

    def set_command_parser(self, command_parser):
        """
        :description
            外部からcommand_parserを挿入する事が出来るインスタンスメソッド
            Noneかどうかを検査する事で、先に代入された方が優先させる事が出来る。
        :param
            command_parser  : AbstractCommandParser     コマンドパーサー
        :return             : None
        """
        if self.app is not None:
            if self.app.command_parser is None:
                self.app.command_parser = command_parser
        else:
            # TODO Exceptionのリファクタ
            raise ValueError("Handlerにおいてappが定義されていません。")

    def set_communicator(self, communicator):
        """
        :description
            外部からcommunicatorを挿入する事が出来るインスタンスメソッド
            Noneかどうかを検査する事で、先に代入された方が優先させる事が出来る。
        :param
            communicator  : AbstractCommunicator  コミュニケータ
        :return           : None
        """
        if self.app is not None:
            if self.app.communicator is None:
                self.app.communicator = communicator
        else:
            # TODO Exceptionのリファクタ
            raise ValueError("Handlerにおいてappが定義されていません。")

    def set_communicator_by_method(self, method):
        """
        :description
            methodによりcommunicatorを選択が出来るインスタンスメソッド
        :param
            method  : str 接続方法を記述したファイル
        :return     : AbstractCommunicator  コミュニケータ
        """
        if self.app is not None:
            if self.app.communicator is None:
                self.set_communicator(TestCommunicator())
            #     if method == "console":
            #         self.set_communicator(SerialCommunicator())
            #     elif method == "telnet":
            #         raise ValueError("現在開発中です。そのため、現在使用可能な接続方法はconsoleのみです。")
            #     elif method == "ssh":
            #         raise ValueError("現在開発中です。そのため、現在使用可能な接続方法はconsoleのみです。")
            #     else:
            #         # TODO Exceptionのリファクタ
            #         raise ValueError("接続方法は{}から選択して下さい。".format(["console", "telnet", "ssh"]))
        else:
            # TODO Exceptionのリファクタ
            raise ValueError("Handlerにおいてappが定義されていません。")

    def set_log_parser(self, log_parser):
        """
        :description
            外部からlog_parserを挿入する事が出来るインスタンスメソッド
            Noneかどうかを検査する事で、先に代入された方が優先させる事が出来る。
        :param
            log_parser  : log_parser  ログパーサー
        :return: None
        """
        if self.app is not None:
            if self.app.log_parser is None:
                self.app.log_parser = log_parser
        else:
            # TODO Exceptionのリファクタ
            raise ValueError("Handlerにおいてappが定義されていません。")

    def set_inventory_parser(self, inventory_parser):
        """
        :description
            外部からinventory_parserを挿入する事が出来るインスタンスメソッド
            Noneかどうかを検査する事で、先に代入された方が優先させる事が出来る。
        :param
            inventory_parser  : inventory_parser  インベントリパーサー
        :return: None
        """
        if self.app is not None:
            if self.app.inventory_parser is None:
                self.app.inventory_parser = inventory_parser
        else:
            # TODO Exceptionのリファクタ
            raise ValueError("Handlerにおいてappが定義されていません。")

    @staticmethod
    @abstractmethod
    def parse_arguments():
        pass

    @abstractmethod
    def handle(self):
        pass





