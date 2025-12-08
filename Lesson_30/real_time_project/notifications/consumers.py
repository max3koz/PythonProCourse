import json
from typing import Any

import aioredis
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
	"""
	WebSocket consumer for push notifications.
	- Each client connects to the `notifications` group.
	- When a message is received from one client, it is sent to all.
	"""
	
	group_name: str = "notifications"
	redis: aioredis.Redis | None = None
	redis_key: str = "notifications_history"
	
	async def connect(self) -> None:
		"""Connecting a client to a group."""
		self.redis = await aioredis.from_url("redis://127.0.0.1:6379")
		await self.channel_layer.group_add(self.group_name, self.channel_name)
		await self.accept()
		
		history = await self.redis.lrange("notifications_history", 0, -1)
		for msg in reversed(history):
			await self.send(
				text_data=json.dumps({"notification": msg.decode()}))
	
	async def disconnect(self, close_code: int) -> None:
		"""Disconnecting a client from a group."""
		await self.channel_layer.group_discard(self.group_name,
		                                       self.channel_name)
	
	async def receive(self,
	                  text_data: str | None = None,
	                  bytes_data: bytes | None = None) -> None:
		"""
		Receives a message from the client and sends it to all subscribers.
		Args: text_data (str | None): JSON string containing the message.
        """
		if text_data and self.redis:
			data: dict[str, Any] = json.loads(text_data)
			message: str = data.get("message", "")
			
			await self.redis.lpush(self.redis_key, message)
			
			await self.channel_layer.group_send(self.group_name,
			                                    {"type": "push_notification",
			                                     "message": message, })
	
	async def push_notification(self, event: dict[str, Any]) -> None:
		"""
		Handles a `push_notification` event and sends it to the client.
		Args: event (dict[str, Any]): Dictionary with key `message'.
        """
		await self.send(
			text_data=json.dumps({"notification": event["message"]}))
