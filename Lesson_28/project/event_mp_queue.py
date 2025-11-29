"""
Event Queue — асинхронне оброблення подій через multiprocessing.Queue.
"""

import multiprocessing
from typing import Any, Callable, Dict


class MPEventQueue:
	"""Event Queue — asynchronous event processing via multiprocessing.Queue."""
	
	def __init__(self) -> None:
		self._queue: "multiprocessing.Queue[Dict[str, Any]]" = multiprocessing.Queue()
		self._processes = []
		self._running = multiprocessing.Value('b', True)
	
	def start_worker(self, handler: Callable[[str, Any], None]) -> None:
		"""
		Runs a worker in a separate process. The worker reads events from
		the queue and processes them.
		"""
		
		def worker(queue: multiprocessing.Queue,
		           running: multiprocessing.Value) -> None:
			while running.value:
				try:
					event = queue.get(timeout=1)
					event_name = event["event"]
					data = event["data"]
					try:
						handler(event_name, data)
					except Exception as e:
						print(
							f"[WORKER ERROR] Помилка при обробці {event_name}: {e}")
				except Exception:
					continue
		
		p = multiprocessing.Process(target=worker,
		                            args=(self._queue, self._running))
		p.daemon = True
		p.start()
		self._processes.append(p)
	
	def stop_workers(self) -> None:
		"""Stops all workers."""
		self._running.value = False
		for p in self._processes:
			p.join(timeout=1)
	
	def put_event(self, event_name: str, data: Any) -> None:
		"""Producer throws an event into the queue."""
		self._queue.put({"event": event_name, "data": data})
