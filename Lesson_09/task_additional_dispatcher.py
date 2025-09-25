from typing import Callable, Any, Dict, List


class EventDispatcher:
	"""
	The plugin-based event dispatcher: stores event handlers and allows
	dispatching events by name.
	Attributes:
	- events (Dict[str, List[Callable[[Any], None]]]):
	  A dictionary mapping event names to lists of handler functions.
	"""
	
	def __init__(self) -> None:
		self.events: Dict[str, List[Callable[[Any], None]]] = {}
	
	def register_event(self, name: str, handler: Callable[[Any], None]) -> None:
		"""
		Registers a handler function for a given event name.
		Parameters:
		- name (str): The name of the event.
		- handler (Callable[[Any], None]): A function that handles the event data.
		"""
		if name not in self.events:
			self.events[name] = []
		self.events[name].append(handler)
	
	def dispatch_event(self, name: str, data: Any) -> None:
		"""
		Dispatches an event by calling all registered handlers with the provided data.
		Parameters:
		- name (str): The name of the event to dispatch.
		- data (Any): The data to pass to each handler.
		"""
		handlers = self.events.get(name, [])
		for handler in handlers:
			handler(data)


def on_message(data: str):
	print(f"Отримано повідомлення: {data}")


dispatcher = EventDispatcher()

dispatcher.register_event("message", on_message)
dispatcher.dispatch_event("message", "First message.")
