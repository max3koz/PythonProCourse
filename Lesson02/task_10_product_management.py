def create_product(product_name: str) -> callable:
	def product_with_price(product_price: float) -> callable:
		def product_with_quantity(product_quantity: int) -> callable:
			product = {"name": product_name,
			           "price": product_price,
			           "quantity": product_quantity
			           }
			
			def change_price(new_price: float) -> str:
				if new_price >= 0:
					product["price"] = new_price
					return (f"The product price for the '{product['name']}' "
					        f"was changed to {new_price}!")
				return f"It is invalid price value!!!"
			
			return change_price
		
		return product_with_quantity
	
	return product_with_price


price_update = create_product("Product_1")(200)(2)
print(price_update(-90))
print(price_update(250))
print(price_update(0.5))
print(price_update(0))
