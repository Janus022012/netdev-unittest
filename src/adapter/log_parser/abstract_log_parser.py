import os
from abc import ABC, abstractmethod

TEMPLATE_DIR = os.path.abspath("../../templates")


class AbstractLogParser(ABC):
    def __init__(self):
        self.device = None
        self.communicator_output_path = []
        self.result = {}

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device):
        self._device = device

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        # 空白を_で結合して文字列に変換
        self._command = "_".join(command.split(" "))

    @property
    def communicator_output_path(self):
        return self._communicator_output_path

    @communicator_output_path.setter
    def communicator_output_path(self, communicator_output_path):
        self._communicator_output_path = communicator_output_path

    @abstractmethod
    def check_template(self, commands):
        pass

    @abstractmethod
    def parse(self):
        pass

    def get_template_file_path(self, command):
        # TODO 暫定処理 textfsm以外の拡張子も認めるように修正
        return os.path.join(
            TEMPLATE_DIR,
            self.device.manufacturer_name,
            self.device.device_name,
            self.device.version,
            command+".textfsm"
        )

    def get_communicator_output_path(self, command):
        if (os.path.basename(self.communicator_output_path).split("%")[-1]).split(".")[0] == "_".join(command.split(" ")):
            return self.communicator_output_path
