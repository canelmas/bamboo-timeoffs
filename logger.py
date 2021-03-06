import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "logs/bamboo-timeoffs.log"
FORMAT = "%(asctime)s %(levelname)s %(name)s [%(filename)s:%(lineno)d]: %(message)s"

logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    datefmt='%m-%d-%Y %H:%M',
                    handlers=[RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8")])


def get_logger():
    return logging.getLogger()
