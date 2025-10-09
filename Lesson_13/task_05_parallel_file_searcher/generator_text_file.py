import os
import random
from typing import List

LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
MESSAGES = [
	"Connection established",
	"User login successful",
	"Disk space low",
	"Timeout occurred",
	"File not found",
	"Permission denied",
	"Critical error: system halted",
	"Background job completed",
	"Memory usage high",
	"Network unreachable"
]


def generate_log_file(filename: str, lines: int = 100_000,
                      error_rate: float = 0.01) -> None:
	"""
	The function generates a log file with random messages.
	Args:
		filename (str): Path to the file.
		lines (int): Number of lines.
		error_rate (float): Frequency of occurrence of "ERROR" (0.0–1.0).
	"""
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, "w", encoding="utf-8") as file:
		for _ in range(lines):
			level = random.choices(LOG_LEVELS,
			                       weights=[1 - error_rate, 0.05, error_rate,
			                                0.1])[0]
			message = random.choice(MESSAGES)
			file.write(f"[{level}] {message}\n")
	print(f"Generated the '{filename}' file with {lines} lines.")


def generate_multiple_logs(folder: str, count: int = 3,
                           lines_per_file: int = 100_000) -> List[str]:
	"""
	The function creates multiple log files in the specified folder.
	Args:
		folder (str): Folder to save.
		count (int): Number of files.
		lines_per_file (int): Lines in each file.
	Returns:
		List[str]: List of paths to the created files.
	"""
	os.makedirs(folder, exist_ok=True)
	files = []
	for i in range(1, count + 1):
		path = os.path.join(folder, f"file_server{i}.log")
		generate_log_file(path, lines=lines_per_file)
		files.append(path)
	return files
