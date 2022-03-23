import os
import textfsm

from .abstract_log_parser import AbstractLogParser


class TextFSMLogParser(AbstractLogParser):
    def __init__(self):
        super().__init__()

    def check_template(self, commands):
        for command in commands:
            reformated_command = "_".join(command.split(" "))
            if not os.path.exists(self.get_template_file_path(reformated_command)):
                # TODO Exception強化=ServerErrorかUserErrorかどうかを明示する。
                raise FileNotFoundError("command: {}のテンプレートファイルが存在しません。\n{}に配置してください。"
                                        .format(reformated_command, self.get_template_file_path(reformated_command)))

    def check_communicator_output_files(self):
        if not self.get_communicator_output_path(self.command):
            # TODO Exception強化=ServerErrorかUserErrorかどうかを明示する。
            raise FileNotFoundError("command: {}の出力ファイルが存在しません。".format(self.command))

    def parse(self):
        self.check_communicator_output_files()

        with open(self.get_template_file_path(self.command), "r") as f:
            parser_template = textfsm.TextFSM(f)
            command_output = open(self.get_communicator_output_path(self.command)).read()
            result = parser_template.ParseText(command_output)
            print(result)
        return [dict(zip(parser_template.header, result_tmp)) for result_tmp in result]
