"""Example usage of EventBus with events and listeners."""

from eventbus import EventBus
from listeners import email_sender, logger, analytics

bus = EventBus()

bus.subscribe("user.registered", email_sender)
bus.subscribe("user.*", logger)
bus.subscribe("order.*", analytics)

bus.emit("user.registered", {"username": "maksym"})
bus.emit("user.deleted", {"username": "john_doe"})
bus.emit("order.created", {"order_id": 123, "amount": 250})

print("\nEvent Log:")
for entry in bus.get_event_log():
    print(entry)
