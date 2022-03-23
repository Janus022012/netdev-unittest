from abc import ABC, abstractmethod


class AbstractApp(ABC):
    def __init__(self):
        """
        properties
        :property _inventory        :   対象となるホスト群を記述したファイル
        :property _cfile            :   実行するコマンド群を記述したファイル
        :property _command_parser   :   実行するコマンドを解釈するインスタンス
        :property _communicator     :   対象との接続を担うインスタンス
        :property _log_parser       :   ログの解釈を担当するインスタンス
        :property _inventory_parser :   インベントリファイルの解釈を担当するインスタンス
        :property
        :property
        :property
        :property
        """
        self._inventory = ""
        self._cfile = ""
        self._command_parser = None
        self._communicator = None
        self._log_parser = None
        self._inventory_parser = None
        self.result_file_path = []
        self.output_file_paths = []

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, inventory):
        self._inventory = inventory

    @property
    def cfile(self):
        return self._cfile

    @cfile.setter
    def cfile(self, cfile):
        self._cfile = cfile

    @property
    def command_parser(self):
        return self._command_parser

    @command_parser.setter
    def command_parser(self, command_parser):
        self._command_parser = command_parser

    @property
    def communicator(self):
        return self._communicator

    @communicator.setter
    def communicator(self, communicator):
        self._communicator = communicator

    @property
    def log_parser(self):
        return self._log_parser

    @log_parser.setter
    def log_parser(self, log_parser):
        self._log_parser = log_parser

    @property
    def inventory_parser(self):
        return self._inventory_parser

    @inventory_parser.setter
    def inventory_parser(self, inventory_parser):
        self._inventory_parser = inventory_parser

    def initialize_adapter(self):
        # TODO try_exceptの追加
        self._command_parser.cfile = self.cfile
        self._inventory_parser.inventory = self.inventory

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def run(self):
        pass
