"""A mini-simulation of an online store with EventBus and event queue."""

import time

from analytics_service import AnalyticsService
from event_queue import EventQueue
from eventbus import EventBus
from notification_service import NotificationService
from order_service import OrderService

bus = EventBus()
event_queue = EventQueue()

order_service = OrderService(bus)
notification_service = NotificationService()
analytics_service = AnalyticsService()

bus.subscribe("order.created", notification_service.send_email)
bus.subscribe("order.created", analytics_service.track_order)
bus.subscribe("order.paid", notification_service.send_sms)
bus.subscribe("order.paid", analytics_service.track_payment)


def event_handler(event_name: str, data: dict) -> None:
	bus.emit(event_name, data)


event_queue.start_worker(event_handler)

event_queue.put_event("order.created",
                      {"order_id": 1, "amount": 100})
event_queue.put_event("order.paid",
                      {"order_id": 1, "amount": 100})
event_queue.put_event("order.created",
                      {"order_id": 2, "amount": 250})
event_queue.put_event("order.paid",
                      {"order_id": 2, "amount": 250})

time.sleep(2)

event_queue.stop_workers()

print("\nЛог подій:")
for entry in bus.get_event_log():
	print(entry)
