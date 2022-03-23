import logging
import sys


def get_logger(file_name: str):
    fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"

    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format=fmt)

    return logger
