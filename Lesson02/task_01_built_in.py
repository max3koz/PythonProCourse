import random


def my_sum() -> None:
	"""
	Create function 'my_sum' which will be cover build-in 'sum' function
	"""
	print("This is my custom 'sum' function!")


first_number = random.randint(0, 5)  # Create list of number
numbers = [number for number in range(first_number,
                                      random.randint(first_number, 10))]
print(f"Creates list of number: {numbers}")
print(f"Built-in sum: {sum(numbers)}")  # Call built-in 'sum' function
sum = my_sum  # Overrides the built-in function by 'my_sum' function
sum()  # Call overrided function 'sum'
try:
	sum(numbers)  # Try use 'sum' function as the build-in function
except TypeError as e:
	print(f"Error: {e}")
	print()
	print("Питання 1: Що відбувається, коли локальна функція має те саме ім'я, "
	      "що й вбудована?")
	print("Відповідь: Локальна функція перекриває вбудовану функцію. "
	      "Таким чином при виклику функції з ім'ям вбудованої функції після її "
	      "перевизначення буде виконуватись алгоритм, який реалізований у "
	      "локальній функції. Вбудована функция викликатися не буде.")
	print("Питання 2: Як можна отримати доступ до вбудованої функції, навіть "
	      "якщо вона перекрита?")
	print("Відповідь: Існує декілька варіантів: "
	      "1. Зберігти оригінал вбудованої функції, до реалізації перекриття.")
	print(
		"                                     2. Використати пакет buildins, "
		"наприклад:")
	print("                                        import buildins ")
	print("                                        builtins.sum([5, 2, 4])")
