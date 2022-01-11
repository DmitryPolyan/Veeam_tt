import logging

log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def file_handler() -> logging.FileHandler:
    """Handler for writing in file """
    file_handler = logging.FileHandler("logs.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    return file_handler


def stream_handler() -> logging.StreamHandler:
    """Handler for console output """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(log_format))
    return stream_handler


def get_logger(name: str) -> logging.getLogger:
    """Logger creation """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler())
    logger.addHandler(stream_handler())
    return logger
