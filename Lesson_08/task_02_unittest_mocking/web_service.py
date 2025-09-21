import requests


class WebService:
	"""
	The class for retrieving data from a website via an HTTP request.
	"""
	
	def get_data(self, url: str) -> dict:
		"""
		Makes a GET request to the specified URL and returns a JSON response.
		Raises:
			requests.RequestException: if the request fails
		"""
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
