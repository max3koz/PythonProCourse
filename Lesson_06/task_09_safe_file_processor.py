import os
import shutil
from typing import TextIO


class SafeFileProcessor:
	"""
	Context manager for secure processing of an important file.
	- Creates a backup copy before processing
	- Opens a temporary file for writing
	- If processing is successful, replaces the original
	- If an error occurs, restores the backup copy
	Parameters:
		filepath: Path to the important file
	"""
	
	def __init__(self, filepath: str) -> None:
		self.filepath = filepath
		self.backup_path = filepath + ".bak"
		self.temp_path = filepath + ".tmp"
		self.temp_file: TextIO | None = None
	
	def __enter__(self) -> TextIO:
		# Create a backup copy
		shutil.copy2(self.filepath, self.backup_path)
		# Open a temporary file for writing
		self.temp_file = open(self.temp_path, "w", encoding="utf-8")
		return self.temp_file
	
	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		if self.temp_file:
			self.temp_file.close()
		
		if exc_type is None:
			# Successfully: replace the original
			shutil.move(self.temp_path, self.filepath)
			os.remove(self.backup_path)
			print(f"The '{self.filepath}' file was updated.")
		else:
			# Error: Restore backup
			shutil.move(self.backup_path, self.filepath)
			if os.path.exists(self.temp_path):
				os.remove(self.temp_path)
			print(f"Processing error. Restored backup ‘{self.backup_path}’.")


test_file = "task_09_important_file.txt"

try:
	with SafeFileProcessor(test_file) as file:
		file.write("Оновлений вміст файлу\n")
		# raise RuntimeError("Imitetion og error!!!")  # Uncomment for negative test
except Exception as e:
	print(f"Exception: {e}")
