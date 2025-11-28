"""A mini-simulation of an online store with EventBus."""

from analytics_service import AnalyticsService
from eventbus import EventBus
from notification_service import NotificationService
from order_service import OrderService

bus = EventBus()

order_service = OrderService(bus)
notification_service = NotificationService()
analytics_service = AnalyticsService()

bus.subscribe("order.created", notification_service.send_email)
bus.subscribe("order.created", analytics_service.track_order)
bus.subscribe("order.paid", notification_service.send_sms)
bus.subscribe("order.paid", analytics_service.track_payment)

order_service.create_order({"order_id": 1, "amount": 100})
order_service.pay_order({"order_id": 1, "amount": 100})

order_service.create_order({"order_id": 2, "amount": 250})
order_service.pay_order({"order_id": 2, "amount": 250})

print("\nЛог подій:")
for entry in bus.get_event_log():
	print(entry)
