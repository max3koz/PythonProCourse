import random
from multiprocessing import Pool, cpu_count
from typing import List, Tuple

TOTAL_NUMBER = random.randint(10_000, 100_000)
NUM_PROCESSES = random.randint(2, cpu_count())


def generate_numbers(count: int, min_val: int = 1,
                     max_val: int = 100) -> List[int]:
	"""
	The function generates a list of random integers.
	Args:
		- count (int): Number of numbers.
		- min_val (int): Minimum value.
		- max_val (int): Maximum value.
	Returns: List[int]: List of random numbers.
	"""
	numbers_list: List[int] = [random.randint(min_val, max_val) for _ in
	                           range(count)]
	print(f"Generated {count} numbers: {numbers_list[:20]} ...")
	return numbers_list


def split_array(array: List[int], parts: int) -> List[List[int]]:
	"""
	The function divides an array into a given number of parts.
	Args:
		array (List[int]): Input array.
		parts (int): Number of parts.
	Returns: List[List[int]]: List of subarrays.
	"""
	part_size = len(array) // parts
	return [array[i * part_size: (i + 1) * part_size] for i in range(parts)]


def sum_part_number(part_num_list: List[int]) -> int:
	"""
	The function calculates the sum of the elements in a subarray.
	Args: part_num_list (List[int]): Subarray of numbers.
	Returns: int: Sum of the elements.
	"""
	result = sum(part_num_list)
	print(f"Sum of part: {result}")
	return result


def parallel_sum(array: List[int], processes: int) -> Tuple[int, List[int]]:
	"""
	The function calculates the sum of an array in parallel across
	multiple processes.
	Args:
		array (List[int]): Input array of numbers.
		processes (int): Number of processes.
	Returns:
		Tuple[int, List[int]]: The total sum and a list of the sums of the parts.
	"""
	parts = split_array(array, processes)
	with Pool(processes=processes) as pool:
		partial_sums = pool.map(sum_part_number, parts)
	total = sum(partial_sums)
	return total, partial_sums


numbers = generate_numbers(TOTAL_NUMBER)

total, partials = parallel_sum(numbers, NUM_PROCESSES)

print(f"\nTotal sum: {total}")
print(f"Sum of the part: {partials}")
