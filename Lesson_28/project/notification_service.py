from typing import Any


class NotificationService:
	"""Notification Service — responds to order events."""
	
	def send_email(self, data: Any) -> None:
		"""Sends an email when an order is created."""
		print(f"[EMAIL] Відправлено лист про створення замовлення: {data}")

	def send_sms(self, data: Any) -> None:
		"""Sends SMS when paying for an order."""
		print(f"[SMS] Відправлено SMS про оплату замовлення: {data}")
