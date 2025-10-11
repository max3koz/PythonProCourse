import asyncio
import sys


async def slow_task() -> None:
	"""The function simulates a slow task that runs for 10 seconds."""
	print("Starting a slow task...")
	await asyncio.sleep(10)
	print("The task completed!")


async def progress_timer() -> None:
	"""Displays a progress timer every second."""
	seconds = 0
	while True:
		await asyncio.sleep(1)
		seconds += 1
		sys.stdout.write(f"\rIt's over.: {seconds} sec")
		sys.stdout.flush()


async def run_with_timeout() -> None:
	"""
	The function calls slow_task() with a timeout of 5 seconds.
	If the task does not complete on time, displays a timeout message.
	"""
	timer_task = asyncio.create_task(progress_timer())
	try:
		await asyncio.wait_for(slow_task(), timeout=5)
	except asyncio.TimeoutError:
		print("\nTimeout: task not completed in 5 seconds.")
	finally:
		timer_task.cancel()
		try:
			await timer_task
		except asyncio.CancelledError:
			print("The timer is stopped.")


asyncio.run(run_with_timeout())
