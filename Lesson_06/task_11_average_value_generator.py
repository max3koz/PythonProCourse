from typing import Iterator


def streaming_average(filename: str) -> Iterator[float]:
	"""
	Generates the current average value of numbers from a large file.
	Parameters:
		filename: Path to a text file where each line is a number
	Return:
		Iterator of average values after each line
	"""
	total = 0.0
	count = 0
	
	try:
		with open(filename, "r", encoding="utf-8") as file:
			for line in file:
				try:
					value = float(line.strip())
					total += value
					count += 1
					yield total / count
				except ValueError:
					print(f"Incorrect value skipped: {line.strip()}")
	except FileNotFoundError:
		print(f"The '{filename}' file is nor found.")


test_file = "task_11_test_data.txt"

for avg in streaming_average(test_file):
	print(f"Current average value: {avg:.2f}")
