import argparse

from .abstract_handler import AbstractHandler
from src.adapter.command_parser.yaml_command_parser import YamlCommandParser
from src.adapter.log_parser.textfsm_log_parser import TextFSMLogParser
from src.adapter.inventory_parser.ini_inventory_parser import IniInventoryParser


USECASES = ["run", "check"]


class CliHandler(AbstractHandler):
    def __init__(self, app):
        super().__init__(app)

    @staticmethod
    def parse_arguments():
        """
        :description
            引数を解析すスタティック関数
        :return     : dictionary    引数の解析後の結果が格納された辞書型変数
        """
        parser = argparse.ArgumentParser("netutest",
                                         description="本プログラムはネットワーク機器の単体テスト自動化を実施するためのプログラムです。")
        subparsers = parser.add_subparsers(help='help for subcommand')

        # 単体試験実行のユースケース
        run_parser = subparsers.add_parser('run', help="単体テストを実行する際に使用します。")
        run_parser.set_defaults(command="run")
        run_parser.add_argument("-c", "--cfile", required=True,
                                help="netutestが実行する内容を記述したファイルのパスを指定してください。")
        run_parser.add_argument("-i", "--inventory", required=True,
                                help="netutestが実行する対象を記述したファイルパスを指定してください。")
        run_parser.add_argument("-m", "--method", choices=["console", "telnet", "ssh"], required=True,
                                help="netutestを実行する機器への接続方法を['console', 'telnet', 'ssh']から選択して下さい。")

        # 単体試験実行前のステータス確認のユースケース
        command_parser = subparsers.add_parser("check",
                                               help="単体テストを実施する前に機器のデフォルト値を確認する際に使用します。")
        command_parser.set_defaults(command="check")
        command_parser.add_argument("-c", "--cfile", required=True,
                                    help="netutestが実行する内容を記述したファイルのパスを指定してください。")
        command_parser.add_argument("-i", "--inventory", required=True,
                                    help="netutestが実行する対象を記述したファイルパスを指定してください。")
        command_parser.add_argument("-m", "--method", required=True, choices=["console", "telnet", "ssh"],
                                    help="netutestを実行する機器への接続方法を['console', 'telnet', 'ssh']から選択して下さい。")

        # 引数の抽出
        args = parser.parse_args()
        return args

    def handle(self):
        """
        :description
        :return: None
        """
        args = self.parse_arguments()

        # commandがrun又はcheckである事の確認
        if "command" in args:
            if args.command not in USECASES:
                raise ValueError("コマンドは{}から選択してください。".format(USECASES))
        else:
            raise ValueError("コマンドは{}から選択してください。".format(USECASES))

        # 属性の確認
        if not self.check_attribution(args):
            raise ValueError("引数に{}が存在しません。\n{}".format(self.REQUIRED_KEYS, args))

        # 事前ファイルの確認
        for input_file_path in [args.cfile, args.inventory]:
            if not self.check_file(input_file_path):
                raise FileNotFoundError("入力として指定されたパス({})にファイルが存在しません。".format(input_file_path))

        # cfile・inventoryのセット
        self.app.cfile = args.cfile
        self.app.inventory = args.inventory

        # TODO テストの実行が容易になるようにこの部分を外部化する。
        # adapter群のセット
        self.set_command_parser(YamlCommandParser())
        self.set_log_parser(TextFSMLogParser())
        self.set_inventory_parser(IniInventoryParser())
        self.set_communicator_by_method(args.method)

        # checkコマンドの実行
        if args.command == "check":
            result = self.app.check()
        # runコマンドの実行
        elif args.command == "run":
            result = self.app.run()
        else:
            raise ValueError("実装していないコマンド({})が指定されました。".format(args.command))

        # 事後ファイルの確認
        for output_file_path in result["result_log"]:
            if not self.check_file(output_file_path):
                raise FileNotFoundError("出力として指定されたパス({})にファイルが存在しません。".format(output_file_path))
