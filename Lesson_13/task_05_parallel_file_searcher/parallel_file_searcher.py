from multiprocessing import Process, Queue
from typing import List

from generator_text_file import generate_multiple_logs


def search_in_file(filename: str, searchable_text: str,
                   result_queue: Queue) -> None:
	"""
	The function searches for text in a file and adds the found lines
	to the result queue.
	Args:
		filename (str): Path to the file.
		searchable_text (str): Text to search for.
		result_queue (Queue): Queue to send results to.
	"""
	try:
		with open(filename, "r", encoding="utf-8", errors="ignore") as f:
			for i, line in enumerate(f, 1):
				if searchable_text in line:
					result_queue.put((filename, i, line.strip()))
	except Exception as e:
		result_queue.put((filename, -1, f"Error: {e}"))


def parallel_search(file_list: List[str], searchable_text: str) -> None:
	"""
	The function runs a parallel text search in a list of files.
	Args:
		file_list (List[str]): List of file paths.
		searchable_text (str): Text to search for.
	"""
	result_queue = Queue()
	processes = []
	
	for file in file_list:
		process = Process(target=search_in_file,
		                  args=(file, searchable_text, result_queue))
		process.start()
		processes.append(process)
	
	for process in processes:
		process.join()
	
	while not result_queue.empty():
		filename, line_num, content = result_queue.get()
		print(f"[{filename}:{line_num}] {content}")


search_text = "ERROR"
files_to_search = generate_multiple_logs("logs", count=3, lines_per_file=30_000)

parallel_search(files_to_search, search_text)
