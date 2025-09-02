import random
import time


def timer(func):
	def wrapper(*args, **kwargs):
		start = time.time()
		result = func(*args, **kwargs)
		end = time.time()
		print(f"Час виконання: {end - start:.6f} sec")
		return result
	
	return wrapper


@timer
def sum_random_numbers():
	list_of_numbers = list(
		map(lambda number: random.randint(1, 100), range(1000)))
	total = sum(list_of_numbers)
	print(f"Sum is {total}.")
	return list_of_numbers


numbers = sum_random_numbers()
