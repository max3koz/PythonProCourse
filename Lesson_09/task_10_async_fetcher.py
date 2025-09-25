import asyncio
from typing import Dict, Any, Awaitable

class AsyncFetcher:
    """
    Asynchronous data fetcher that simulates an HTTP request.
    Methods:
    - fetch(url: str) -> Awaitable[Dict[str, Any]]:
      Simulates fetching data from a given URL and returns a dictionary.
    """

    async def fetch(self, url: str) -> Dict[str, Any]:
        """
        Simulates an asynchronous HTTP GET request.
        Parameters:
        - url (str): The URL to fetch data from.
        Returns:
        - Dict[str, Any]: Simulated response data.
        """
        await asyncio.sleep(1)  # simulate network delay
        return {
            "url": url,
            "status": 200,
            "data": {"message": "This is a mock response"}
        }


async def main():
    fetcher = AsyncFetcher()
    result = await fetcher.fetch("https://example.com/api")
    print(result)

asyncio.run(main())
