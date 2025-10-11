import asyncio
import sys

from aiohttp import web


async def handle_root(request: web.Request) -> web.Response:
	"""
	The function processes the route '/' and returns plain text.
	Args: request (web.Request): Incoming HTTP request.
	Returns: web.Response: Response with the text "Hello, World!".
	"""
	return web.Response(text="Hello, World!")


async def handle_slow(request: web.Request) -> web.Response:
	"""
	The function processes the '/slow' route, simulating a long operation
	with a delay of 5 seconds.
	Returns: web.Response: Response with the text "Operation completed"
	after the delay.
	"""
	await asyncio.sleep(5)
	return web.Response(text="Operation completed")


def create_app() -> web.Application:
	"""
	The function creates and configures an aiohttp web application with routes.
	Returns: web.Application: The configured web application.
	"""
	app = web.Application()
	app.router.add_get("/", handle_root)
	app.router.add_get("/slow", handle_slow)
	return app


def main() -> None:
	port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
	app = create_app()
	web.run_app(app, port=8081)

if __name__ == "__main__":
	main()
