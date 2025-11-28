"""Example of using Event Replay."""

from eventbus_replay import EventBus
from notification_service import NotificationService
from analytics_service import AnalyticsService

bus = EventBus()
notification_service = NotificationService()
analytics_service = AnalyticsService()

bus.subscribe("order.created", notification_service.send_email)
bus.subscribe("order.created", analytics_service.track_order)
bus.subscribe("order.paid", notification_service.send_sms)
bus.subscribe("order.paid", analytics_service.track_payment)

bus.replay_from_file("events.log")
