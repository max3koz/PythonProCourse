import asyncio
from typing import Any


async def producer(queue: asyncio.Queue, num_consumers: int) -> None:
	"""
	The function adds 5 tasks to the queue at 1 second intervals.
	Args:
		queue (asyncio.Queue): Queue for tasks
        num_consumers (int): The number of consumers that will process tasks
        from the queue.
    """
	for i in range(1, 6):
		await asyncio.sleep(1)
		task = f"Task {i}"
		await queue.put(task)
		print(f"Added to the queue: {task}")
	for item in range(num_consumers):
		await queue.put(None)


async def consumer(queue: asyncio.Queue, name: str) -> None:
	"""
	The function takes tasks from the queue and processes them
	with a delay of 2 seconds.
	Args:
		queue (asyncio.Queue): Queue for tasks.
		name (str): Consumer name for identification.
	"""
	while True:
		task: Any = await queue.get()
		if task is None:
			print(f"!!! The {name} consumer has completed the task.")
			break
		print(f"!! The {name} consumer processes: {task}")
		await asyncio.sleep(2)
		print(f"!! The {name} consumer has completed: {task}")
		queue.task_done()


async def main(num_consumers = 2) -> None:
	"""
	The function launches a producer and multiple consumers simultaneously
	to process tasks from the queue.
	"""
	queue: asyncio.Queue = asyncio.Queue()
	consumers = [consumer(queue, f"consumer-{i + 1}") for i in range(2)]
	await asyncio.gather(producer(queue, num_consumers), *consumers)


asyncio.run(main())
