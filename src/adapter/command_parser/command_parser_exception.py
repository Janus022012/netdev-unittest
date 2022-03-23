#TODO 暫定処置 → constにまとめる？
CHECK_REQUIRED_KEYS = ["commands"]


class CommandParserException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class CommandParserCheckInvalidKeyError(CommandParserException):
    def __str__(self):
        return "必須のディレクティブである{}のいづれかが含まれていません。".format(CHECK_REQUIRED_KEYS)


class CommandParserCheckInvalidNumberError(CommandParserException):
    def __str__(self):
        return "commands配下の確認コマンド数が0です。"
