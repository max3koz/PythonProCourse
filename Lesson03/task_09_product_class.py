import pytest

from assertpy import assert_that


class ProductWithGetSet:
	"""
	Product class with getters and setters for price.
	"""
	
	def __init__(self, name: str, price: float) -> None:
		self.name: str = name
		self._price: float = 0.0
		self.set_price(price)
	
	def get_price(self) -> float:
		"""Returns the price of the product."""
		return self._price
	
	def set_price(self, value: float) -> None:
		"""Sets the price of the product. Checks that it is not negative."""
		if value < 0:
			raise ValueError("The price cannot be negative.")
		self._price = value


class ProductWithProperty:
	"""
	Product class using the @property decorator for price.
	"""
	
	def __init__(self, name: str, price: float) -> None:
		self.name: str = name
		self._price: float = 0.0
		self.price = price
	
	@property
	def price(self) -> float:
		"""Returns the price of the product."""
		return self._price
	
	@price.setter
	def price(self, value: float) -> None:
		"""Sets the price of the product. Checks that it is not negative."""
		if value < 0:
			raise ValueError("The price cannot be negative.")
		self._price = value


class PriceDescriptor:
	"""
	Descriptor for controlling access to price.
	"""
	
	def __init__(self, currency: str = "EUR") -> None:
		self._name = "_price"
		self.currency = currency
	
	def __get__(self, instance: object, owner: type) -> float:
		return getattr(instance, self._name)
	
	def __set__(self, instance: object, value: float) -> None:
		if value < 0:
			raise ValueError("The price cannot be negative.")
		setattr(instance, self._name, value)


class ProductWithDescriptor:
	"""Product class with a descriptor for price."""
	
	price = PriceDescriptor()
	
	def __init__(self, name: str, price: float) -> None:
		self.name: str = name
		self.price = price


class CurrencyDescriptor:
	"""A descriptor that converts the price depending on the currency."""
	exchange_rates = {
		"EUR": 1.0,
		"USD": 1.1,
		"PLN": 4.5
	}
	
	def __init__(self, name: str = "_price") -> None:
		self._name = name
	
	def __get__(self, instance: object, owner: type) -> float:
		if instance is None:
			return self
		raw = getattr(instance, self._name)
		currency = getattr(instance, "currency",
		                   "EUR")  # ← читаємо валюту з об'єкта
		rate = self.exchange_rates.get(currency, 1.0)
		return round(raw * rate, 2)
	
	def __set__(self, instance: object, value: float) -> None:
		if value < 0:
			raise ValueError("The price cannot be negative.")
		setattr(instance, self._name, value)


class ProductWithCurrency:
	"""Product with price descriptor and currency support."""
	price = CurrencyDescriptor()
	
	def __init__(self, name: str, price: float, currency: str = "EUR") -> None:
		self.name = name
		self.currency = currency
		self.price = price


@pytest.mark.parametrize("test_product_name, test_price, test_new_price", [
	pytest.param("Book", 100, 120,
	             id="TC_09_01: Verify the price and increase update price function"),
	pytest.param("Laptop", 1500, 1400,
	             id="TC_09_02: Verify the price and decrease update price function"),
	pytest.param("Smartphone", 800, -850,
	             id="TC_09_03: Verify the price is negative")
])
def test_update_product_price(test_product_name: str,
                              test_price: float,
                              test_new_price: float) -> None:
	product = ProductWithGetSet(test_product_name, test_price)
	if test_new_price < 0:
		with pytest.raises(ValueError):
			ProductWithGetSet(test_product_name, test_new_price)
	else:
		assert_that(product.get_price() == test_price,
		            f"Error: price value: expected: {test_price}, "
		            f"actual:{product.get_price()}").is_true()
		product.set_price(test_new_price)
		assert_that(product.get_price() == test_new_price,
		            f"Error: price value: expected: {test_price}, "
		            f"actual:{product.get_price()}").is_true()


@pytest.mark.parametrize("test_value, test_currency, expected_result", [
	pytest.param(100, "PLN", 450,
	             id="TC_09_04: Verify the price in PLN"),
	pytest.param(100, "USD", 110,
	             id="TC_09_05: Verify the price in PLN"),
	pytest.param(100, "EURO", 100,
	             id="TC_09_06: Verify the price in PLN"),
	pytest.param(-100, "PLN", None,
	             id="TC_09_07: Verify the price is negative")
])
def test_products_price_converter(test_value: float,
                                  test_currency: str,
                                  expected_result: float) -> None:
	if test_value < 0:
		with pytest.raises(ValueError):
			ProductWithCurrency("Headset", test_value, currency=test_currency)
	else:
		product = ProductWithCurrency("Headset", test_value,
		                              currency=test_currency)
		assert_that(product.price == expected_result,
		            f"Error: unexpected result: {product.price}, "
		            f"actual_result: {expected_result}").is_true()


"""
Сеттери/геттери:
Перевага: явна логика;
Недолік: більше коду.

Проперті:
Перевага: пайтон стиль кодуб легка читаємость;
Недолік: меньш гнучкий та не має можливості перевикористати.

Дескріптори:
Перевага: контроль над доступом, можливість перевикористовувати,
можливість підтримки складної логіки;
Недолік: складний синтаксис, код не очевидний з точки зору роботи коду.

я вибрав деструктор, тому що:
Він дозволяє читати валюту з об'єкта і застосовувати курс при кожному доступі до ціни;
Логіка конверсії валют знаходиться в одному місці - легко використовувати;
Є можливість легко додати нові валюти, форматування.
"""
