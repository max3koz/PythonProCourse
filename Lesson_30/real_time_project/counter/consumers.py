import json
from typing import Any

import aioredis
from channels.generic.websocket import AsyncWebsocketConsumer


class OnlineCounterConsumer(AsyncWebsocketConsumer):
	"""
	WebSocket consumer for counting online users in real time.
		- Uses Redis to store a global counter.
		- Increments the value on each connection.
		- Decrements the value on each disconnect.
		- Broadcasts the updated counter to all clients in the online_counter`group.
	"""
	group_name: str = "online_counter"
	
	async def connect(self) -> None:
		"""
		Called when a new WebSocket connection is established.
			- Connects the Redis client.
			- Adds the channel to the group.
			- Accepts the connection.
			- Increments the online user counter.
			- Broadcasts the updated value to all clients.
		"""
		self.redis = await aioredis.from_url("redis://127.0.0.1:6379")
		await self.channel_layer.group_add(self.group_name, self.channel_name)
		await self.accept()
		
		await self.redis.incr("online_users_count")
		await self._broadcast_count()
	
	async def disconnect(self, close_code) -> None:
		"""
		Called when a WebSocket connection is closed.
			- Removes the channel from the group.
			- Decrements the online users counter.
			- Broadcasts the updated value to all clients.
		"""
		await self.channel_layer.group_discard(self.group_name,
		                                       self.channel_name)
		await self.redis.decr("online_users_count")
		await self._broadcast_count()
	
	async def update_count(self, event: dict[str, Any]) -> None:
		"""
		Handles the `update_count` event sent via the group.
		Sends a JSON with the number of online users to the client.
		Args: event (dict[str, Any]): Dictionary with the key `count'.
		"""
		await self.send(text_data=json.dumps({"online_users": event["count"]}))
	
	async def _broadcast_count(self) -> None:
		"""
		Gets the current counter value from Redis and sends it to all clients
		in the group.
		"""
		count = await self.redis.get("online_users_count")
		count = int(count) if count else 0
		await self.channel_layer.group_send(self.group_name,
		                                    {"type": "update_count",
		                                     "count": count})
