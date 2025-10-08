import sys
from multiprocessing import Pool, cpu_count
from typing import List, Tuple


def part_range(num: int, parts: int) -> List[Tuple[int, int]]:
	"""
	Розбиває діапазон [1, n] на піддіапазони для паралельного обчислення.

	Args:
		num (int): Число, факторіал якого обчислюється.
		parts (int): Кількість процесів.

	Returns:
		List[Tuple[int, int]]: Список пар (start, end) для кожного процесу.
	"""
	step = num // parts
	ranges = []
	for i in range(parts):
		start = i * step + 1
		end = (i + 1) * step if i < parts - 1 else num
		ranges.append((start, end))
	return ranges


def partial_product(start: int, end: int) -> int:
	"""
	Calculates the product of numbers in the range [start, end].
	Args:
		start (int): Start of the range.
		end (int): End of the range.
	Returns: int: Product of the numbers.
	"""
	result = 1
	for i in range(start, end + 1):
		result *= i
	return result


def parallel_factorial(f_number: int) -> int:
	"""
	Calculates the factorial of a large number using multiple processes.
	Args: n (int): The number whose factorial to calculate.
	Returns: int: The factorial of n.
	"""
	if f_number < 0:
		raise ValueError(
			"The factorial is defined only for non-negative integers.")
	if f_number == 0 or f_number == 1:
		return 1
	
	num_processes = min(cpu_count(), f_number)
	ranges = part_range(f_number, num_processes)
	
	with Pool(processes=num_processes) as pool:
		partial_results = pool.starmap(partial_product, ranges)
	
	factorial_result = 1
	for part in partial_results:
		factorial_result *= part
	return factorial_result


def save_to_file(factorial_number: int, filename: str) -> None:
	"""
	Saves the factorial to a text file.
	Args:
		factorial_number (int): The factorial to write.
		filename (str): The filename.
	"""
	with open(filename, "w") as f:
		f.write(str(factorial_number))


number = 100_000
sys.set_int_max_str_digits(number * 10)
print(f"Calculating the factorial of a number {number}...")

result = parallel_factorial(number)
print(f"Factorial the {number} number has {len(str(result))} number.")

result_file = "factorial_result.txt"
save_to_file(result, result_file)
print(f"Result saved to file - '{result_file}'")
