from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, List, Optional


class RoundedDecimal:
	"""
	Descriptor for automatically rounding Decimal to 2 decimal places.
	"""
	
	def __init__(self, name: str) -> None:
		"""
		Initializes a handle with the name of an attribute.
		Args: name (str): The name of the attribute to be processed.
		"""
		self.name = "_" + name
	
	def __get__(self, instance: Any, owner: type) -> Decimal:
		"""
		Returns the rounded value of the attribute.
		Args: instance: The instance of the class containing the attribute,
		owner: The owner's class.
		Returns: Decimal: The rounded value.
		"""
		return getattr(instance, self.name)
	
	def __set__(self, instance, value):
		"""
		Sets the value of an attribute, rounded to two digits.
		Args: instance: An instance of the class.
		value: The value to round.
		"""
		decimal_value = Decimal(value)
		rounded = decimal_value.quantize(Decimal("0.01"),
		                                 rounding=ROUND_HALF_UP)
		setattr(instance, self.name, rounded)


class Price:
	"""
	The class that represents the price of a product to two decimal places.
	"""
	
	amount = RoundedDecimal("amount")
	
	def __init__(self, value: float | str | Decimal) -> None:
		"""
		Initializes the Price object.
		Args: value: Initial price value (float, str or Decimal).
		"""
		self.amount = value
	
	"""Dunder methods with expected behavior"""
	
	def __repr__(self) -> str:
		return f"Price({self.amount:.2f})"
	
	def __add__(self, other: "Price") -> "Price":
		return Price(self.amount + other.amount)
	
	def __sub__(self, other: "Price") -> "Price":
		return Price(self.amount - other.amount)
	
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Price):
			return NotImplemented
		return self.amount == other.amount
	
	def __lt__(self, other: "Price") -> bool:
		return self.amount < other.amount
	
	def __le__(self, other: "Price") -> bool:
		return self.amount <= other.amount
	
	def __gt__(self, other: "Price") -> bool:
		return self.amount > other.amount
	
	def __ge__(self, other: "Price") -> bool:
		return self.amount >= other.amount
	
	def to_float(self) -> float:
		"""Converts a price value to a float. Returns: float: The price value."""
		return float(self.amount)
	
	@classmethod
	def from_float(cls, value: float) -> "Price":
		"""
		Creates a Price object from a string.
		Args: value (str): A string representation of the price.
		Returns: Price: A new Price object.
		"""
		return cls(Decimal(str(value)))


class Transaction:
	"""
	Represents a single financial transaction.
	Attributes:
		id (str): Unique transaction identifier.
		amount (Price): Transaction amount.
		status (str): Transaction status ("success", "failed", "pending").
		timestamp (datetime): Time the transaction was created.
	"""
	
	_counter = 0
	
	def __init__(self, amount: Price, status: str,
	             timestamp: Optional[datetime] = None) -> None:
		Transaction._counter += 1
		self.id: str = f"Tr/{Transaction._counter}"
		self.amount: Price = amount
		self.status: str = status
		self.timestamp: datetime = timestamp or datetime.now()
	
	def __repr__(self) -> str:
		"""
		Returns a string representation of a transaction.
		Returns: str:
		Format "<Transaction <self.id> | <self.amount> | <self.status> | <self.timestamp>>"
		"""
		return (
			f"<Transaction {self.id} | {self.amount.to_float()} | "
			f"{self.status} | {self.timestamp.isoformat()}>"
		)


class PaymentGateway:
	"""
	The class for processing financial transactions using Price.
	"""
	
	def __init__(self, balance: Price, currency: str = "EUR") -> None:
		self.balance: Price = balance
		self.currency: str = currency
		self.transactions: List[Transaction] = []
	
	def deposit(self, amount: Price) -> None:
		"""
		Top up the balance by the specified amount.
		Args: amount (Price): Amount to top up.
		"""
		self.balance = self.balance + amount
		self._log_transaction(amount, "deposit")
	
	def process_payment(self, amount: Price) -> bool:
		"""
		Processes the payment if there are sufficient funds.
		Args: amount (Price): Amount to be paid.
		Returns: bool: True if the payment is successful.
		"""
		if self.balance >= amount:
			self.balance = self.balance - amount
			self._log_transaction(amount, "success")
			return True
		else:
			self._log_transaction(amount, "failed")
			return False
	
	def convert_currency(self, rate: Decimal, target_currency: str) -> None:
		"""
		Converts the balance to a new currency.
		Args:
			rate (Decimal): Conversion rate.
			target_currency (str): New currency.
		"""
		converted = self.balance.amount * rate
		self.balance = Price(converted)
		self.currency = target_currency
	
	def _log_transaction(self, amount: Price, status: str) -> None:
		"""
		Transaction logging.
		Args:
			amount (Price): Transaction amount.
			status (str): Status ("success", "failed").
		"""
		self.transactions.append(Transaction(amount, status))
	
	def get_transaction_history(self) -> List[Transaction]:
		"""
		Returns a list of all transactions.
		Returns: List[Transaction]: Transaction history.
		"""
		return self.transactions
	
	def get_balance_amount(self) -> float:
		"""
		Returns the balance as a number (float).
		Returns: float: The balance value.
		"""
		return self.balance.to_float()


"""The sentences of the use classes PaymentGateway and Price"""

gateway = PaymentGateway(balance=Price("0.00"))

gateway.deposit(Price("150.00"))
gateway.process_payment(Price("25.50"))
gateway.process_payment(Price("90.00"))

print("List of transaction:")
for tx in gateway.get_transaction_history():
	print(tx)
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("Amount of the balance:")
print(f"Balance in $:   {gateway.get_balance_amount()}")
gateway.convert_currency(Decimal("45"), "$")
print(f"Balance in UAH: {gateway.get_balance_amount()}")
