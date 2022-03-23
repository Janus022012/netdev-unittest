import yaml


from .abstract_command_parser import AbstractCommandParser
from .command_parser_exception import CommandParserCheckInvalidKeyError, CommandParserCheckInvalidNumberError


class YamlCommandParser(AbstractCommandParser):
    CHECK_REQUIRED_KEYS = ["commands"]
    RUN_REQUIRED_KEYS = ["states", "procedure"]

    def __init__(self):
        super().__init__()

    def parse(self):
        self.commands = self.read_command_parser(self.cfile)
        return self.commands

    def write(self, result, file_path):
        with open(file_path, "w") as f:
            yaml.dump(result, f, default_flow_style=False)

    def validate_check_method_syntax(self):
        yaml_file = self.read_command_parser(self.cfile)

        # トップレベルのディレクティブにcommands以外存在しないか
        if not all([True if key in self.CHECK_REQUIRED_KEYS else False for key in yaml_file.keys()]):
            raise CommandParserCheckInvalidKeyError()

        # 複数のコマンドが登録されているか
        if not len(yaml_file["commands"]):
            raise CommandParserCheckInvalidNumberError()

    def validate_run_method_syntax(self):
        pass

    @staticmethod
    def read_command_parser(file_path):
        file = open(file_path, "r")
        return yaml.safe_load(file)