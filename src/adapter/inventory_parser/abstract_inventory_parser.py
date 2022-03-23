from abc import ABC, abstractmethod


class AbstractInventoryParser(ABC):
    """
    本クラスは、インベントリファイルのパーサーを定義する抽象クラスである。
    """

    REQUIRED_KEYS = ("host_name", "ip_address", "manufacturer_name", "device_name", "version", "port_name", "baudrate",
                     "login_id", "login_password", "admin_password")

    def __init__(self):
        self._inventory = None
        self._hosts = []

    @property
    def hosts(self):
        return self._hosts
    
    @hosts.setter
    def hosts(self, hosts):
        self._hosts = hosts

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, inventory):
        self._inventory = inventory

    def check_required_keys(self, keys):
        return all([True if key in keys else False for key in self.REQUIRED_KEYS])

    @abstractmethod
    def parse(self):
        pass