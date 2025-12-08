import asyncio

import aioredis
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
	"""
	Django AppConfig for the `notifications` application.
		- Runs on Django/ASGI startup.
		- Clears the `notifications_history` key in Redis so that notification
		history is not persisted across server restarts.
		- Uses an asynchronous task via an event loop to avoid blocking startup.
	"""
	default_auto_field = "django.db.models.BigAutoField"
	name = "notifications"
	
	def ready(self) -> None:
		"""
		Called automatically when Django starts.
		Creates an asynchronous task to clear the Redis key `notifications_history`.
		"""
		
		async def clear_notifications() -> None:
			"""
			Asynchronous function to clear the `notifications_history` key in Redis.
			Executed once at server startup.
			"""
			redis = await aioredis.from_url("redis://127.0.0.1:6379")
			await redis.delete("notifications_history")
		
		loop = asyncio.get_event_loop()
		loop.create_task(clear_notifications())
