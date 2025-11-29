from typing import Any

from eventbus import EventBus


class OrderService:
	"""Order Service — generates order events."""
	
	def __init__(self, bus: EventBus) -> None:
		self.bus = bus


	def create_order(self, order_data: Any) -> None:
		"""Creates an order and generates the 'order.created' event."""
		print(f"[ORDER] Створено замовлення: {order_data}")
		self.bus.emit("order.created", order_data)

	def pay_order(self, payment_data: Any) -> None:
		"""Pays for the order and generates the 'order.paid' event."""
		print(f"[ORDER] Оплачено замовлення: {payment_data}")
		self.bus.emit("order.paid", payment_data)
