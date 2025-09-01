DISCOUNT = 0.2
VIP_DISCOUNT = 0.1


def create_order(price: float) -> None:
	"""
	A function that takes the price of the product as an argument and internally:
	- calculates the final price taking into account the discount defined globally;
	- nested function apply_additional_discount, which adds an additional discount
	and changes the final price.
	"""
	final_price = price * (1 - DISCOUNT)  # local variable? price after discount
	print(f"Price after global discount: {final_price}")
	
	def apply_additional_discount() -> None:
		"""
		The function adds an additional discount and changes the final price
		"""
		nonlocal final_price
		final_price *= (1 - VIP_DISCOUNT)
	
	apply_additional_discount()
	print(f"Final price with additional discount: {final_price}")


create_order(100)
print()
create_order(5000)
