import asyncio
from colorama import Fore, Back, Style

async def load_website():
	task = asyncio.create_task(fetch_data())
	print("Doing another thing...")
	print("Another thing while waiting...")
	return_value = await task
	print(f"success in loading data from:{return_value}")


async def fetch_data():
	print("fetching data...")
	await asyncio.sleep(4)
	return Fore.GREEN + " data from the server"

asyncio.run(load_website())