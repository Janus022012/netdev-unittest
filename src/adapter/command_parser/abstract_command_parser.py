from abc import ABC, abstractmethod


class AbstractCommandParser(ABC):
    """
    :description
        本クラスは、コマンドファイルのパーサーを定義する抽象クラスである。
    """
    def __init__(self):
        self.commands = {}
        self.cfile = None

    @property
    def commands(self):
        return self._commands
    
    @commands.setter
    def commands(self, commands):
        self._commands = commands

    @property
    def cfile(self):
        return self._cfile

    @cfile.setter
    def cfile(self, cfile):
        self._cfile = cfile

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def write(self, result, file_path):
        pass

    @abstractmethod
    def validate_check_method_syntax(self):
        pass

    @abstractmethod
    def validate_run_method_syntax(self):
        pass

    @staticmethod
    @abstractmethod
    def read_command_parser(file_path):
        pass