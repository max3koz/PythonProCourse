import zipfile
from typing import Optional


class ZipArchiver:
	"""
	Context manager for creating a ZIP archive.
	On entry — opens the archive for writing.
	On exit — automatically closes the archive.
	Parameters:
		archive_name: Name of the ZIP file
		mode: Archiving mode (‘w’ — create new, ‘a’ — append to existing)
	"""
	
	def __init__(self, archive_name: str, mode: str = "w") -> None:
		self.archive_name = archive_name
		self.mode = mode
		self.zip: Optional[zipfile.ZipFile] = None
	
	def __enter__(self) -> "ZipArchiver":
		self.zip = zipfile.ZipFile(self.archive_name,
		                           mode=self.mode,
		                           compression=zipfile.ZIP_DEFLATED)
		print(f"Archive '{self.archive_name}' opened in the "
		      f"'{self.mode}' mode.")
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		if self.zip:
			self.zip.close()
			print(f"Archive '{self.archive_name}' closed successfully.")
	
	def add_file(self, filepath: str, arcname: Optional[str] = None) -> None:
		"""
		Adds a file to the archive.
		Parameters:
			filepath: Path to the file on disk
			arcname: Name of the file in the archive (optional)
		"""
		if self.zip is None:
			raise RuntimeError("Archive was not opened.")
		self.zip.write(filepath, arcname=arcname or filepath)
		print(f"Added the file: {filepath}")


test_file = "task_10_test_file.txt"
archive_file = "task_10_test_archive.zip"

with ZipArchiver(archive_file) as archiver:
	archiver.add_file(test_file)
	archiver.add_file(test_file, arcname=f"{test_file}_config.json")
