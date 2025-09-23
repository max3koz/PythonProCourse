import pytest
from assertpy import assert_that


def calculate_discount(price: float, discount: float) -> float:
	"""
	Calculates the final price after applying a discount.
	Parameters:
	- price (float): The original price of the item.
	- discount (float): The discount percentage to apply.
	Returns:
	- float: The final price after discount. Returns 0.0 if discount exceeds 100%.
	"""
	if discount > 100:
		return 0.0
	return price * (1 - discount / 100)


@pytest.mark.parametrize("test_price, test_discount, expected_result", [
	pytest.param(100, 20, 80.00, id="TC01_01: discount less then 100%"),
	pytest.param(100, 99, 1.00, id="TC01_02: discount 99%"),
	pytest.param(100, 100, 0.00, id="TC01_03: discount 100%"),
	pytest.param(100, 101, 0.00, id="TC01_04: discount 101%")
])
def test_function_calculate_discount(test_price: float, test_discount: float,
                                     expected_result: float):
	actual_result = calculate_discount(test_price, test_discount)
	assert_that(actual_result).is_close_to(expected_result, tolerance=0.001)
