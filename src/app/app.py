import os
from datetime import datetime
from .abstract_app import AbstractApp


OUTPUTS_DIR = os.path.abspath("../../outputs")


class App(AbstractApp):
    def __init__(self):
        super().__init__()

    def check(self):
        # 結果
        result = {"command_log": [], "result_log": []}

        # adapter群の初期化
        self.initialize_adapter()

        # inventory_parserのバリデーション
        self.inventory_parser.validate_syntax()
        # inventory_parserの解析
        devices = self.inventory_parser.parse()

        # command_parserのバリデーション
        self.command_parser.validate_check_method_syntax()
        # command_parserの解析
        # TODO 専用のオブジェクト化
        commands = self.command_parser.parse()

        for device in devices:
            # log_parserにdeviceのセット
            self.log_parser.device = device
            # log_parserのテンプレートチェック
            self.log_parser.check_template(commands["commands"])

            # communicatorにdeviceのセット
            self.communicator.device = device
            # communicatorの通信チェック
            self.communicator.validate_communicator()

            # アウトプットの格納先の作成
            log_dir = os.path.join(OUTPUTS_DIR, "log_{}".format(datetime.now().strftime("%Y%m%d%H%M%S")))
            command_log_dir = os.path.join(log_dir, "command_log")
            result_log_dir = os.path.join(log_dir, "result")
            os.mkdir(log_dir)
            os.mkdir(command_log_dir)
            os.mkdir(result_log_dir)

            # コマンドの取得
            for command in commands["commands"]:
                reformated_command = "_".join(command.split(" "))
                command_log_path = os.path.join(command_log_dir, "{}%{}.log".format(device, reformated_command))
                command_status_path = os.path.join(result_log_dir, "{}%{}.log".format(device, reformated_command))

                with open(command_log_path, "w") as clf:
                    clf.write(self.communicator.communicate(command))

                # log_parserにテンプレートファイルをセット
                self.log_parser.command = command
                # log_parserにoutputの格納先をセット
                self.log_parser.communicator_output_path = command_log_path
                # log_parserによるログの解析
                parser_result = self.log_parser.parse()
                # log_parserによる解析結果のYAMLファイル化
                self.command_parser.write({command: {"status": parser_result}}, command_status_path)

                # 結果の格納
                result["command_log"].append(command_log_path)
                result["result_log"].append(command_status_path)

        return result

    def run(self):
        pass