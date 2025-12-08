from __future__ import annotations

import json
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
	"""
	WebSocket consumer for authenticated chat.
		- Shows username in messages.
		- Prevents guests (anonymous users) from sending messages.
	"""
	group_name: str = "chat"
	
	async def connect(self) -> None:
		"""Connecting a user to a chat group."""
		await self.channel_layer.group_add(self.group_name, self.channel_name)
		await self.accept()
	
	async def disconnect(self, close_code: int) -> None:
		"""Disconnecting a user from a chat group."""
		await self.channel_layer.group_discard(self.group_name,
		                                       self.channel_name)
	
	async def receive(self, text_data: str | None = None,
	                  bytes_data: bytes | None = None) -> None:
		"""
		Receives a message from the client.
			- If the user is authenticated → sends it to everyone.
			- If the user is a guest → ignores or sends a warning.
		"""
		if not self.scope["user"].is_authenticated:
			await self.send(text_data=json.dumps({
				"error": "❌ Гостям заборонено писати повідомлення."}))
			return
		
		if text_data:
			data: dict[str, Any] = json.loads(text_data)
			message: str = data.get("message", "")
			
			username: str = self.scope["user"].username
			
			await self.channel_layer.group_send(
				self.group_name,
				{
					"type": "chat_message",
					"message": message,
					"username": username,
				}
			)
	
	async def chat_message(self, event: dict[str, Any]) -> None:
		"""
		Handles the `chat_message` event and sends it to the client.
		Args: event (dict[str, Any]): Dictionary with keys `message`and username.
		"""
		await self.send(text_data=json.dumps({
			"username": event["username"],
			"message": event["message"],
		}))
