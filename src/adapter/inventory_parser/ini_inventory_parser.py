import configparser

from .abstract_inventory_parser import AbstractInventoryParser
from .inventory_parser_exception import InventoryParserSectionInvalidKeyError
from src.domain.entity.device import Device


class IniInventoryParser(AbstractInventoryParser):
    """
    本クラスは、インベントリファイルのパーサーを定義する具象クラスである。
    """

    def __init__(self):
        super().__init__()

    def parse(self):
        inventory = self.read_config_parser(self.inventory)

        for section in inventory.sections():
            section_keys = inventory.options(section) + ["host_name"]
            if not self.check_required_keys(section_keys):
                raise InventoryParserSectionInvalidKeyError(section)
            else:
                args = {key: inventory.get(section, key) for key in inventory.options(section)}
                args.update({"host_name": section})

                # TODO deviceの作成方法の検討
                device = Device(args["host_name"], args["ip_address"], args["manufacturer_name"],
                                args["device_name"], args["version"], args["port_name"], args["baudrate"],
                                args["login_id"], args["login_password"], args["admin_password"])
                self.hosts.append(device)
        return self.hosts

    def validate_syntax(self):
        inventory = self.read_config_parser(self.inventory)

        # セクションに必要な変数が書き込まれているか
        for section in inventory.sections():
            section_keys = inventory.options(section) + ["host_name"]
            if not self.check_required_keys(section_keys):
                raise InventoryParserSectionInvalidKeyError(section)

        # TODO 必要な変数において誤った値が割り当てられていないか

    @staticmethod
    def read_config_parser(path):
        inventory = configparser.ConfigParser()
        inventory.read(path, encoding="utf-8")
        return inventory
