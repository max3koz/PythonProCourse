import pytest

from assertpy import assert_that


class InsufficientFundsException(Exception):
	"""
	The exception that occurs when there are insufficient funds to complete
	a financial transaction.
	Attributes:
		required_amount (float): The amount required to complete the transaction.
		current_balance (float): The current account balance.
		currency (str, optional): The account currency.
		transaction_type (str, optional): Transaction type (e.g., “withdrawal,”
		“purchase”).
	"""
	
	def __init__(
			self,
			required_amount: float,
			current_balance: float,
			currency: str = "UAH",
			transaction_type: str = "unknown"
	) -> None:
		self.required_amount = required_amount
		self.current_balance = current_balance
		self.currency = currency
		self.transaction_type = transaction_type
		super().__init__(self.__str__())
	
	def __str__(self) -> str:
		return (
			f"Insufficient funds for the transaction '{self.transaction_type}'. "
			f"Need: {self.required_amount:.2f} {self.currency}, "
			f"on account: {self.current_balance:.2f} {self.currency}."
		)


def perform_transaction(balance: float, amount: float, currency: str = "UAH",
                        transaction_type: str = "purchase") -> str:
	"""
	Performs a financial transaction if there are sufficient funds in the account.
	Args:
		balance (float): Current account balance.
		amount (float): Transaction amount.
		currency (str): Account currency.
		transaction_type (str): Transaction type.
	Raises:
		InsufficientFundsException: If there are insufficient funds.
	"""
	if balance < amount:
		raise InsufficientFundsException(
			required_amount=amount,
			current_balance=balance,
			currency=currency,
			transaction_type=transaction_type
		)
	transaction_event_log = (
		f"Transaction ‘{transaction_type}’ for {amount:.2f} {currency} "
		f"has been successfully completed.")
	return transaction_event_log


# Test suite
@pytest.mark.parametrize("test_balans_value, test_transaction_value, "
                         "test_transaction_type, expected_result", [
	                         pytest.param(250, 200, "withdrawal",
	                                      "Transaction ‘withdrawal’ for 200.00 UAH has been successfully completed.",
	                                      id="TC_04_06: positive test_case"),
	                         pytest.param(150, 200, "withdrawal",
	                                      "Insufficient funds for the transaction 'withdrawal'. Need: 200.00 UAH, on account: 150.00 UAH.",
	                                      id="TC_04_07: negative testcase.")
                         ])
def test_insufficient_resource(test_balans_value, test_transaction_value,
                               test_transaction_type, expected_result):
	try:
		action_resource_log = perform_transaction(balance=test_balans_value,
		                                          amount=test_transaction_value,
		                                          transaction_type=test_transaction_type)
	except InsufficientFundsException as e:
		action_resource_log = str(e)
	
	assert_that(action_resource_log == expected_result,
	            f"Error: expected result: {expected_result}, "
	            f"actual result: {action_resource_log}").is_true()
