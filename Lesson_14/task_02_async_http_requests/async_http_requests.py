import asyncio
from typing import List, Union

import aiohttp


async def fetch_content(url: str) -> Union[str, None]:
	"""
	The function makes an HTTP request to the specified URL and returns
	the page content.
	Args: url (str): The address of the web page to load.
	Returns: Union[str, None]: The page content as text or an error message.
	"""
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(url, timeout=10) as response:
				response.raise_for_status()
				content: str = await response.text()
				print(f"Successfully uploaded: {url}")
				return content
	except aiohttp.ClientError as e:
		print(f"Error while loading {url}: {e}")
		return None
	except asyncio.TimeoutError:
		print(f"Timeout when loading {url}")
		return None


async def fetch_all(urls: List[str]) -> List[Union[str, None]]:
	"""
	The function downloads the contents of all pages from a list of URLs in parallel.
	Args: urls (List[str]): List of web addresses to download.
	Returns: List[Union[str, None]]: List of page contents or error messages.
	"""
	tasks: List[asyncio.Task] = [asyncio.create_task(fetch_content(url))
	                             for url in urls]
	results: List[Union[str, None]] = await asyncio.gather(*tasks)
	return results


test_urls = [
	"https://example.com",
	"https://google.com",
	"https://nonexistent.domain",
	"https://httpstat.us/404",
	"https://ukr.net"
]

asyncio.run(fetch_all(test_urls))
