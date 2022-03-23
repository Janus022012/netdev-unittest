from abc import ABC, abstractmethod


class AbstractCommunicator(ABC):
    """
    AbstractCommunicator
    """
    def __init__(self):
        self._device = None

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device):
        self._device = device

    @abstractmethod
    def validate_communicator(self):
        pass

    @abstractmethod
    def check_access(self):
        pass

    @abstractmethod
    def check_communication(self):
        pass

    @abstractmethod
    def check_login(self):
        pass

    @abstractmethod
    def login(self, session):
        pass

    @abstractmethod
    def admin_login(self, session):
        pass

    @abstractmethod
    def communicate(self, command):
        pass

    @abstractmethod
    def logout(self, session):
        pass
