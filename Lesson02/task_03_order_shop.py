DISCOUNT = 0.2
VIP_DISCOUNT = 0.1


def create_order(price: float) -> None:
	final_price = price * (1 - DISCOUNT)  # local variable? price after discount
	print(f"Price after global discount: {final_price}")
	
	def apply_additional_discount() -> None:
		nonlocal final_price
		final_price *= (1 - VIP_DISCOUNT)
	
	apply_additional_discount()
	print(f"Final price with additional discount: {final_price}")


create_order(100)
print()
create_order(5000)
