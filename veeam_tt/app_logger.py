import logging

log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


class Logger:
    def __init__(self, name, log_path):
        """Logger creation """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(Logger.file_handler(log_path))
        logger.addHandler(Logger.stream_handler())

    @staticmethod
    def file_handler(log_path: str) -> logging.FileHandler:
        """Handler for writing in file """
        file_handler = logging.FileHandler(f"{log_path}/logs.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(log_format))
        return file_handler

    @staticmethod
    def stream_handler() -> logging.StreamHandler:
        """Handler for console output """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(log_format))
        return stream_handler
