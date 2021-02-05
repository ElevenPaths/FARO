import logging
import logging.handlers
from pathlib import Path


class Logger:

    def __init__(self, logger_name, file_name, logging_level=logging.DEBUG, max_bytes=1000000, backup_count=3):
        self.separator = " -- "
        formatter = logging.Formatter('%(asctime)s -- %(message)s')
        self.my_logger = logging.getLogger(logger_name)
        self.my_logger.setLevel(logging_level)
        file_log = Path(__file__).parent.parent / "logs" / file_name
        handler = logging.handlers.RotatingFileHandler(file_log, maxBytes=max_bytes, backupCount=backup_count)
        handler.setFormatter(formatter)
        self.my_logger.addHandler(handler)

    def debug(self, file_name, method_name, message):
        error_msg = "DEBUG" + self.separator + file_name + self.separator + method_name + self.separator + message
        self.my_logger.debug(error_msg)

    def info(self, file_name, method_name, message):
        error_msg = "INFO" + self.separator + file_name + self.separator + method_name + self.separator + message
        self.my_logger.info(error_msg)

    def error(self, file_name, method_name, message):
        error_msg = "ERROR" + self.separator + file_name + self.separator + method_name + self.separator + message
        self.my_logger.error(error_msg)

    def warning(self, file_name, method_name, message):
        error_msg = "WARNING" + self.separator + file_name + self.separator + method_name + self.separator + message
        self.my_logger.warning(error_msg)

    def critical(self, file_name, method_name, message):
        error_msg = "CRITICAL" + self.separator + file_name + self.separator + method_name + self.separator + message
        self.my_logger.critical(error_msg)
