import fnmatch
import json
from typing import Callable, Dict, List, Any, Set


class EventBus:
	"""
	A simple EventBus that supports:
		- Subscribing to events (with wildcard support)
		- Unsubscribing from events
		- Emitting events with data
		- Logging all emitted events
	"""
	
	def __init__(self) -> None:
		self._subscribers: Dict[str, Set[Callable[[Any], None]]] = {}
		self._wildcard_subscribers: Dict[str, Set[Callable[[Any], None]]] = {}
		self._event_log: List[Dict[str, Any]] = []
	
	def subscribe(self, event_name: str,
	              callback: Callable[[Any], None]) -> None:
		"""Subscribe a callback to an event."""
		if "*" in event_name:
			self._wildcard_subscribers.setdefault(event_name, set()).add(
				callback)
		else:
			self._subscribers.setdefault(event_name, set()).add(callback)
	
	def unsubscribe(self, event_name: str,
	                callback: Callable[[Any], None]) -> None:
		"""Unsubscribe a callback from an event."""
		if "*" in event_name:
			if event_name in self._wildcard_subscribers:
				self._wildcard_subscribers[event_name].discard(callback)
		else:
			if event_name in self._subscribers:
				self._subscribers[event_name].discard(callback)
	
	def emit(self, event_name: str, data: Any) -> None:
		"""
		Emit an event with associated data.
		Triggers all matching subscribers (including wildcard).
		Logs the event.
		"""
		# Log the event
		event = {"event": event_name, "data": data}
		self._event_log.append(event)
		
		# Save to file
		with open("events.log", "a", encoding="utf-8") as f:
			f.write(json.dumps(event) + "\n")
		
		# Call subscribers
		if event_name in self._subscribers:
			for callback in self._subscribers[event_name]:
				callback(data)
		
		for pattern, callbacks in self._wildcard_subscribers.items():
			if fnmatch.fnmatch(event_name, pattern):
				for callback in callbacks:
					callback(data)
	
	def get_event_log(self) -> List[Dict[str, Any]]:
		"""Return the list of all emitted events."""
		return self._event_log
