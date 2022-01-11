import argparse
import os
import time

import app_logger
import filecmp
import shutil

logger = app_logger.get_logger(__name__)


def get_arguments() -> tuple:
    """
    Getting paths to folders and timing to check from the command line.
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

    def check_timing(timing: str) -> int:
        """ Checking that a digit is entered  """
        if timing.isdigit():
            return int(timing)
        logger.error("Not a number entered")
        raise argparse.ArgumentTypeError("Not a number entered")

    parser = argparse.ArgumentParser(
        description="The utility copies files according to the provided configuration file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("origin_folder", type=check_path, help="Path to origin folder")
    parser.add_argument("repl_folder", type=check_path, help="Path to replica folder")
    parser.add_argument("timing_for_refresh", type=check_timing, help="Timing for refresh folders")
    args = parser.parse_args()
    return args.origin_folder, args.repl_folder, args.timing_for_refresh


def update_repl_content(origin_folder: str, repl_folder: str, origin_name: str) -> None:
    """ Updating changed data """
    logger.info(f"Copy {origin_folder}/{origin_name} to {repl_folder}")
    shutil.copy2(f"{origin_folder}/{origin_name}", f"{repl_folder}")


def append_new_content_int_repl(origin_folder: str, origin_name: str, repl_folder: str) -> None:
    """ Add new data from source folder to replica folder """
    if os.path.isdir(f"{origin_folder}/{origin_name}"):
        logger.info(f"Copy folder {origin_folder}/{origin_name} to {repl_folder}")
        # shutil.copytree(f"{origin_folder}/{origin_name}", f"{repl_folder}/")
    else:
        logger.info(f"Copy {origin_folder}/{origin_name} to {repl_folder}")
        shutil.copy2(f"{origin_folder}/{origin_name}", f"{repl_folder}")


def del_unnecessary_content(unnecessary_data_names: list, repl_folder: str) -> None:
    """ Removing from replica folder data that is not in the original folder """
    for i in unnecessary_data_names:
        if os.path.isdir(f"{repl_folder}/{i}"):
            logger.info(f"Delete {repl_folder}/{i} folder")
            os.rmdir(f"{repl_folder}/{i}")
        else:
            logger.info(f"Delete {repl_folder}/{i} file")
            os.remove(f"{repl_folder}/{i}")


def compare_folder_contents(origin_folder: str, repl_folder: str) -> None:
    content_origin_folder = os.listdir(origin_folder)
    content_repl_folder = os.listdir(repl_folder)
    for origin_name in content_origin_folder:
        if origin_name in content_repl_folder:
            content_repl_folder.remove(origin_name)
            if os.path.isdir(f"{origin_folder}/{origin_name}"):
                logger.info(f"Checking folder {origin_folder}/{origin_name}")
                compare_folder_contents(f"{origin_folder}/{origin_name}", f"{repl_folder}/{origin_name}")
            else:
                if not filecmp.cmp(f"{origin_folder}/{origin_name}", f"{repl_folder}/{origin_name}", shallow=False):
                    update_repl_content(origin_folder, repl_folder, origin_name)
        elif origin_name not in content_repl_folder:
            append_new_content_int_repl(origin_folder, origin_name, repl_folder)
    del_unnecessary_content(content_repl_folder, repl_folder)


def main():
    logger.info("Application started")
    origin_folder, repl_folder, timing_for_refresh = get_arguments()
    logger.info(f"origin_folder {origin_folder}, repl_folder {repl_folder}, timing_for_refresh {timing_for_refresh}")
    # while True:
    #     time.sleep(timing_for_refresh)
    #     compare_folder_contents(origin_folder, repl_folder)
    compare_folder_contents(origin_folder, repl_folder)


if __name__ == '__main__':
    main()


