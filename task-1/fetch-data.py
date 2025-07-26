# Import the requests module
import aiohttp
import asyncio
import json

base_url = 'https://jsonplaceholder.typicode.com'
resource_endpoints = ['posts', 'comments', 'users']

async def fetch_data(url):
    try:
        # Create an asynchronous session
        async with aiohttp.ClientSession() as session:
            # Send a GET request to the desired API URL
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()  # Raise an error for bad responses
                # Parse the response and return it
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")

async def main():
    for endpoint in resource_endpoints:
        url = f"{base_url}/{endpoint}"
        data = await fetch_data(url)
        if data:
            # Log the fetched data
            print(f"Data from {endpoint}:")
            # save the data to mongodb
            print(json.dumps(data, indent=2))
            print("\n")

asyncio.run(main())