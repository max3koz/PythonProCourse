from django.http import HttpRequest, HttpResponse


class CustomHeaderMiddleware:
	"""
	Middleware that adds an 'X-Custom-Header' header to each response.
	The header can be used for custom identification or diagnostics.
	"""
	def __init__(self, get_response):
		"""
		Initialize middleware.
		Args: get_response: Function that processes the request and returns
		the response.
		"""
		self.get_response = get_response
	
	def __call__(self, request: HttpRequest) -> HttpResponse:
		"""
		Processes a request and adds a header to the response.
		Args: request (HttpRequest): Incoming HTTP request.
		Returns: HttpResponse: Response with additional headers.
		"""
		response = self.get_response(request)
		response['X-Custom-Header'] = 'MyValue'
		return response


class RequestCounterMiddleware:
	"""
	Middleware that counts the number of requests processed.
	Prints the number of requests to the console with each call.
	"""
	counter: int = 0
	
	def __init__(self, get_response):
		"""
		Initialize middleware.
		Args: get_response: Function that processes the request and returns
		the response.
		"""
		self.get_response = get_response
	
	def __call__(self, request: HttpRequest) -> HttpResponse:
		"""
		Increments the request counter and prints it to the console.
		Args: request (HttpRequest): Incoming HTTP request.
		Returns: HttpResponse: The response without changes.
		"""
		RequestCounterMiddleware.counter += 1
		print(f"Requests: {RequestCounterMiddleware.counter}")
		return self.get_response(request)
