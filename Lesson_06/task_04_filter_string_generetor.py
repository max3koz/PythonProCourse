from typing import Iterator


def filter_lines_by_keyword(filename: str, keyword: str) -> Iterator[str]:
	"""
	The generator that reads a file line by line and returns only those lines
	that contain a keyword.
	Parameters:
		filename (str): Path to the input text file
		keyword (str): Keyword to search for
	Returns:
		Iterator[str]: Filtered lines
	"""
	try:
		with open(filename, "r", encoding="utf-8") as file:
			for line in file:
				if keyword in line:
					yield line.rstrip("\n")
	except FileNotFoundError:
		print(f"'{filename}' file was not found.")
	except Exception as e:
		print(f"Read eror: {e}")


def save_filtered_lines(input_file: str, output_file: str,
                        keyword: str) -> None:
	"""
	Saves lines from the input file containing a keyword to a file.
	Parameters:
		input_file (str): Path to the input file
		output_file (str): Path to the output file
		keyword (str): Keyword for filtering
	"""
	try:
		with open(output_file, "w", encoding="utf-8") as out:
			for line in filter_lines_by_keyword(input_file, keyword):
				out.write(line + "\n")
		print(
			f"Strings with '{keyword}' keyword were saved to {output_file} file")
	except Exception as e:
		print(f"Write error: {e}")


save_filtered_lines("example.txt",
                    "keyword_only.txt",
                    "35")
