import asyncio

import aioredis
from django.apps import AppConfig


class CounterConfig(AppConfig):
	"""
	Configuration of the `counter` application.
	When Django starts (the `ready` method), an asynchronous reset_counter()
	is executed, which resets the `online_users_count` key in Redis to zero.
	"""
	default_auto_field: str = "django.db.models.BigAutoField"
	name: str = "counter"
	
	def ready(self) -> None:
		"""
		Called when Django starts. Runs the asynchronous reset_counter function
		to reset the counter.
		"""
		
		async def reset_counter() -> None:
			"""
	        Asynchronous function to reset the `online_users_count` key in Redis.
	        Used at project startup.
	        """
			redis = await aioredis.from_url("redis://127.0.0.1:6379")
			await redis.set("online_users_count", 0)
		
		asyncio.run(reset_counter())
