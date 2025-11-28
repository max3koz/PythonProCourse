import queue
import threading
from typing import Any, Callable, Dict


class EventQueue:
	"""Event Queue — asynchronous event processing via queue.Queue."""
	
	def __init__(self) -> None:
		self._queue: "queue.Queue[Dict[str, Any]]" = queue.Queue()
		self._workers = []
		self._running = False
	
	def start_worker(self, handler: Callable[[str, Any], None]) -> None:
		"""
		Starts a worker that reads events from the queue and processes them.
		The worker does not crash on errors.
		"""
		self._running = True
		
		def worker() -> None:
			while self._running:
				try:
					event = self._queue.get(timeout=1)
					event_name = event["event"]
					data = event["data"]
					try:
						handler(event_name, data)
					except Exception as e:
						print(
							f"[WORKER ERROR] Помилка при обробці {event_name}: {e}")
				except queue.Empty:
					continue
		
		t = threading.Thread(target=worker, daemon=True)
		t.start()
		self._workers.append(t)
	
	def stop_workers(self) -> None:
		"""Stops all workers."""
		self._running = False
		for t in self._workers:
			t.join(timeout=1)
	
	def put_event(self, event_name: str, data: Any) -> None:
		"""Producer throws an event into the queue."""
		self._queue.put({"event": event_name, "data": data})
