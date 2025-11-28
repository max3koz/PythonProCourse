from typing import Any


class AnalyticsService:
	"""Analytics Service — counts the number of orders and payments."""
	def __init__(self) -> None:
		self.orders_count = 0
		self.payments_count = 0
	
	def track_order(self, data: Any) -> None:
		"""Increases the order counter."""
		self.orders_count += 1
		print(f"[ANALYTICS] Кількість замовлень: {self.orders_count}")
	
	def track_payment(self, data: Any) -> None:
		"""Increments the payment counter."""
		self.payments_count += 1
		print(f"[ANALYTICS] Кількість оплат: {self.payments_count}")
