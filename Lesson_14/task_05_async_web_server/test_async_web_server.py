import asyncio
import os
import signal
import subprocess
import time

import aiohttp
import pytest
from assertpy import assert_that

BASE_URL = "http://localhost:8081"


@pytest.fixture(scope="module", autouse=True)
def start_server():
	"""
	The fixture starts the server before the tests, checks its readiness,
	and shuts it down after the tests.
	"""
	server_process = subprocess.Popen(
		["python", "Lesson_14/task_05_async_web_server/async_web_server.py",
		 "8081"],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		preexec_fn=os.setsid
	)
	
	success = False
	for _ in range(10):
		try:
			if asyncio.run(ping_server()):
				success = True
				break
		except Exception:
			pass
		time.sleep(0.1)
	
	if not success:
		os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
		stderr_output = server_process.stderr.read().decode()
		print("The server is not responde. STDERR:\n", stderr_output)
		pytest.fail("!!! The server has not started in 1 sec !!!")
	
	yield
	
	os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
	server_process.wait()


async def ping_server() -> bool:
	"""The function sends a request to / and returns True if the server responded."""
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{BASE_URL}/", timeout=1) as resp:
				return resp.status == 200
	except Exception:
		return False


@pytest.mark.asyncio
async def test_parallel_requests():
	"""Verify that requests to '/' and '/slow' are processed in parallel."""
	async with aiohttp.ClientSession() as session:
		start_time = time.perf_counter()
		
		async def get_root():
			async with session.get(f"{BASE_URL}/") as resp:
				text = await resp.text()
				assert_that(resp.status == 200).is_true()
				assert_that(text == "Hello, World!").is_true()
		
		async def get_slow():
			async with session.get(f"{BASE_URL}/slow") as resp:
				text = await resp.text()
				assert_that(resp.status == 200).is_true()
				assert_that(text == "Operation completed").is_true()
		
		await asyncio.gather(get_root(), get_slow())
		
		actual_time = time.perf_counter()
		elapsed = actual_time - start_time
		print(f"\rTotal time: {elapsed:.2f} seconds")
		assert_that(elapsed < 5.03,
		            "Requests were not processed in parallel").is_true()


@pytest.mark.asyncio
async def test_parallel_requests_with_timing():
	"""
	Verify that requests to '/' and '/slow' start at the same time.
	Logs the start and completion time of each request.
	"""
	async with aiohttp.ClientSession() as session:
		timestamps = {}
		
		async def get_root():
			timestamps["root_start"] = time.perf_counter()
			async with session.get(f"{BASE_URL}/") as resp:
				timestamps["root_end"] = time.perf_counter()
				text = await resp.text()
				assert resp.status == 200
				assert text == "Hello, World!"
		
		async def get_slow():
			timestamps["slow_start"] = time.perf_counter()
			async with session.get(f"{BASE_URL}/slow") as resp:
				timestamps["slow_end"] = time.perf_counter()
				text = await resp.text()
				assert resp.status == 200
				assert text == "Operation completed"
		
		await asyncio.gather(get_root(), get_slow())
		
		print("\rThe request '/' started:", timestamps["root_start"])
		print("The request '/' finished:", timestamps["root_end"])
		print("The request '/slow' started:", timestamps["slow_start"])
		print("The request '/slow' finished:", timestamps["slow_end"])
		
		assert_that(timestamps["root_start"] < timestamps["slow_end"],
		            "The request '/' did not start before completion "
		            "'/slow'").is_true()
		
		start_diff = abs(
			timestamps["root_start"] - timestamps["slow_start"])
		assert_that(start_diff < 0.3,
		            f"The requests did not start at the same time "
		            f"(difference {start_diff:.4f} sec)").is_true()
