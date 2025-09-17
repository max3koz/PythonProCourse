from math_utils import factorial, gcd
from string_utils import to_upper, trim_whitespace


def main():
	"""Math utils is running"""
	executed_number = 10
	print(f"The factorial of the number {executed_number} is:"
	      f" {factorial(executed_number)}.")
	first_number, second_number = 48, 18
	print(f"The GCD of numbers {first_number} and {second_number} is: "
	      f"{gcd(first_number, second_number)}.")
	
	"""String utils is running"""
	test_text = "   Hello everyone! "
	print(f"Upper register: '{to_upper(test_text)}'.")
	print(f"Trimmed text: before - '{test_text}' and "
	      f"after to run function - '{trim_whitespace(test_text)}'.")
	
if __name__ == "__main__":
	main()