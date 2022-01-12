import argparse
import os
import time
import filecmp
import shutil
import sys
import inspect

# Solved problem with pytest (ModuleNotFoundError: No module named 'app_logger')
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import app_logger
logger = app_logger.get_logger(__name__)


def get_arguments() -> tuple:
    """
    Getting paths to folders and refresh time period from the command line.
    :return: tuple(path_origin: str, path_repl: str, time_of_check: int)
    """
    def check_path(path: str) -> str:
        """Checking a folder """
        if not os.path.isdir(path):
            logger.error("Folder does not exist")
            raise argparse.ArgumentTypeError("Folder does not exist")
        while path[-1] == '/':
            path = path[:-1]
        return path

    def check_refresh_time_period(refresh_time_period: str) -> int:
        """ Checking that a digit is entered  """
        if refresh_time_period.isdigit():
            return int(refresh_time_period)
        logger.error("Not a number entered")
        raise argparse.ArgumentTypeError("Not a number entered")

    parser = argparse.ArgumentParser(
        description="The utility copies files according to the provided configuration file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("origin_folder", type=check_path, help="Path to origin folder")
    parser.add_argument("repl_folder", type=check_path, help="Path to replica folder")
    parser.add_argument("refresh_time_period", type=check_refresh_time_period, help="Time period for refresh folders")
    args = parser.parse_args()
    return args.origin_folder, args.repl_folder, args.refresh_time_period


def update_repl_content(origin_folder: str, repl_folder: str, original_name: str) -> None:
    """ Updating changed data """
    logger.info(f"Copy {origin_folder}/{original_name} to {repl_folder}")
    shutil.copy2(f"{origin_folder}/{original_name}", f"{repl_folder}")


def append_new_content_int_repl(origin_folder: str, original_name: str, repl_folder: str) -> None:
    """ Add new data from source folder to replica folder """
    if os.path.isdir(f"{origin_folder}/{original_name}"):
        logger.info(f"Copy folder {origin_folder}/{original_name} to {repl_folder}")
        shutil.copytree(f"{origin_folder}/{original_name}", f"{repl_folder}/{original_name}")
    else:
        logger.info(f"Copy {origin_folder}/{original_name} to {repl_folder}")
        shutil.copy2(f"{origin_folder}/{original_name}", f"{repl_folder}")


def del_unnecessary_content(unnecessary_data_names: list, repl_folder: str) -> None:
    """ Removing from replica folder data that is not in the original folder """
    for i in unnecessary_data_names:
        if os.path.isdir(f"{repl_folder}/{i}"):
            logger.info(f"Delete {repl_folder}/{i} folder")
            shutil.rmtree(f"{repl_folder}/{i}", ignore_errors=True)
        else:
            logger.info(f"Delete {repl_folder}/{i} file")
            os.remove(f"{repl_folder}/{i}")


def handling_folder_contents(origin_folder: str, repl_folder: str) -> None:
    """Comparison of content in folders and handling"""
    content_origin_folder = os.listdir(origin_folder)
    content_repl_folder = os.listdir(repl_folder)
    for original_name in content_origin_folder:
        if original_name in content_repl_folder:
            content_repl_folder.remove(original_name)
            if os.path.isdir(f"{origin_folder}/{original_name}"):
                logger.info(f"Checking folder {origin_folder}/{original_name}")
                handling_folder_contents(f"{origin_folder}/{original_name}", f"{repl_folder}/{original_name}")
            else:
                if not filecmp.cmp(f"{origin_folder}/{original_name}", f"{repl_folder}/{original_name}", shallow=False):
                    update_repl_content(origin_folder, repl_folder, original_name)
        elif original_name not in content_repl_folder:
            append_new_content_int_repl(origin_folder, original_name, repl_folder)
    del_unnecessary_content(content_repl_folder, repl_folder)


def main():
    logger.info("Application started")
    origin_folder, repl_folder, refresh_time_period = get_arguments()
    logger.info(f"origin_folder {origin_folder}, repl_folder {repl_folder}, refresh_time_period {refresh_time_period}")
    while True:
        handling_folder_contents(origin_folder, repl_folder)
        time.sleep(refresh_time_period)
        logger.info("Checking restart")


if __name__ == '__main__':
    main()


