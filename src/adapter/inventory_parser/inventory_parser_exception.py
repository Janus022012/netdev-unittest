
# 暫定処置
REQUIRED_KEYS = ("host_name", "ip_address", "manufacturer_name", "device_name", "version", "port_name", "baudrate",
                 "login_id", "login_password", "admin_password")


class InventoryParserException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class InventoryParserSectionInvalidKeyError(InventoryParserException):
    def __str__(self):
        #TODO どれが含まれていないのか特定する。
        return "{}に、必須の引数である{}のいずれかが含まれていません。".format(self.arg, REQUIRED_KEYS)