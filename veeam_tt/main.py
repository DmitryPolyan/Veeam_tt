import argparse
import os


def get_arguments() -> tuple:
    """
    Getting paths to folders and timing to check from the command line.
    :return: tuple(path_origin: str, path_repl: str, time_of_check: int)
    """
    def check_path(path: str) -> str:
        """Checking a folder """
        if not os.path.isdir(path):
            raise argparse.ArgumentTypeError("Folder does not exist")
        return path

    def check_timing(timing: str) -> int:
        """ Checking that a digit is entered  """
        if timing.isdigit():
            return int(timing)
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


def main():
    print(get_arguments())


main()

