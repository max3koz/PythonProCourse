import re
from typing import Iterator


def error_log_lines(filename: str) -> Iterator[str]:
    """
    Generates only those lines from the log file that contain HTTP
    status codes 4XX or 5XX.
    Parameter: filename: Path to the log file
    Return: Iterator of lines with errors
    """
    pattern = re.compile(r'"[A-Z]+\s[^"]+"\s(4\d{2}|5\d{2})\s')

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if pattern.search(line):
                    yield line.rstrip("\n")
    except FileNotFoundError:
        print(f"'{filename}' file was not found.")
    except Exception as e:
        print(f"Reading error: {e}")


def save_errors_to_file(input_file: str, output_file: str) -> None:
    """
	Saves all lines with HTTP errors to a separate file marked [ERROR].
    Parameters:
        input_file: Path to the log file
        output_file: Path to the error file
    """
    try:
        with open(output_file, "w", encoding="utf-8") as out:
            for line in error_log_lines(input_file):
                out.write(f"{line}\n")
        print(f"Errors items are recorded in a file: {output_file}")
    except Exception as e:
        print(f"Writing error: {e}")


log_file = "task_07_test_log_file.log"
parsed_log_file = "parsed_log_error_data.log"

save_errors_to_file(log_file, parsed_log_file)
