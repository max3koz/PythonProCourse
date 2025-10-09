import socket
import threading
from typing import Tuple


class SimpleWebServer:
	"""
	The simple multi-threaded HTTP server that responds to requests with
	a text message.
	"""
	
	def __init__(self, host: str = "0.0.0.0", port: int = 8080):
		self.host = host
		self.port = port
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.running = False
		self.ready_event = threading.Event()
		self.stop_event = threading.Event()
	
	def start(self) -> None:
		"""
		The function starts the server and accepts clients in separate threads.
		"""
		self.server_socket.bind((self.host, self.port))
		self.server_socket.listen(20)
		self.running = True
		self.ready_event.set()  # ✅ Сервер готовий
		print(f"The server is starting on: {self.host}:{self.port}!!!")
		
		while self.running:
			conn, addr = self.server_socket.accept()
			thread = threading.Thread(target=self.handle_client,
			                          args=(conn, addr), daemon=True)
			thread.start()
	
	def stop(self) -> None:
		"""The function stops the server."""
		self.running = False
		self.stop_event.set()
		socket.socket().connect_ex((self.host, self.port))
		self.server_socket.close()
		print("The server is stopped!!!")
	
	def handle_client(self, conn: socket.socket, addr: Tuple[str, int]) -> None:
		"""
		The function processes the client request and sends an HTTP response.
		Args:
			conn (socket.socket): The client socket.
			addr (Tuple[str, int]): The client IP address and port.
		"""
		try:
			request = conn.recv(1024).decode("utf-8")
			print(f"\nRequest from {addr}:\n{request.splitlines()[0]}")
			
			response_body = "Hello! The server is running without error!"
			response = (
				"HTTP/1.1 200 OK\r\n"
				"Content-Type: text/plain; charset=utf-8\r\n"
				f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
				"Connection: close\r\n"
				"\r\n"
				f"{response_body}"
			)
			
			conn.sendall(response.encode("utf-8"))
		except Exception as e:
			print(f"Error: {addr}: {e}")
		finally:
			conn.close()
			print(f"The connection is closed: {addr}")
