from src.app.app import App
from src.adapter.handler.cli_handler import CliHandler
from src.utils.logger_utils import get_logger

Logger = get_logger(__name__)


def main():
    # try:
    # app定義
    app = App()
    # handler定義
    handler = CliHandler(app)
    # handler実行
    handler.handle()
    # except Exception as e:
    #     print(e)


if __name__ == '__main__':
    main()