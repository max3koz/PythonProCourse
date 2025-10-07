import socket
import threading

import pytest

from .web_server import SimpleWebServer


@pytest.fixture(scope="module")
def start_test_server():
	server = SimpleWebServer(host="127.0.0.1", port=9090)
	thread = threading.Thread(target=server.start, daemon=True)
	thread.start()
	server.ready_event.wait(timeout=10)
	assert server.ready_event.is_set(), "The server has not started within 10 sec!"
	yield server
	server.stop()


def test_server_response(start_test_server):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(("127.0.0.1", 9090))
	client.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
	response = client.recv(1024).decode("utf-8")
	client.close()
	
	assert "HTTP/1.1 200 OK" in response
	assert "Hello! The server is running without error!" in response


def test_multiple_clients(start_test_server):
	responses = []
	lock = threading.Lock()
	request = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
	
	def client_task():
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(("127.0.0.1", 9090))
		sock.sendall(request)
		data = sock.recv(1024).decode("utf-8")
		with lock:
			responses.append(data)
		sock.close()
	
	threads = [threading.Thread(target=client_task) for _ in range(10)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	
	assert len(responses) == 10
	for response in responses:
		assert "HTTP/1.1 200 OK" in response
