def add_expense(expense_value: float) -> None:
	global total_expense
	if expense_value < 0:
		print("Warning: the expense cannot be negative!!!")
		return
	total_expense += expense_value
	print(f"Added: {expense_value} UAH.")


def get_expense() -> float:
	return total_expense


def expensive_tracker() -> None:
	print("The expense tracker  is running!!!")
	print("Use commands:")
	print("  - add <value>- to add expense;")
	print("  - total - get total expense;")
	print("  - exit - close expense tracker.")
	while True:
		user_input = input(">>> ").strip()
		
		if user_input.lower() == "exit":
			print("The tracker has finished working!!!")
			break
		elif user_input.lower() == "total":
			print(f"Total expense is: {get_expense()} UAH.")
		elif user_input.lower().startswith("add"):
			try:
				expense_value = float(user_input.split()[1])
				add_expense(expense_value)
			except (IndexError, ValueError):
				print("Error: is not correct the 'add' command!!!")
		else:
			print("Error: Unexpected command. Use 'add <value>', "
			      "'total' or 'exit'!!!")


total_expense = 0.0
expensive_tracker()
