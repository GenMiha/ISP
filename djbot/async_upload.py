import asyncio
import aiohttp
import json


urls_list = None
with open('urls.json', 'r') as file:
    urls_list = json.load(file)

resulting_data = []


async def download_data(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.read()
        resulting_data.append(json.loads(data.decode('utf-8')))
        return data


futures = [download_data(url) for url in urls_list]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))

with open(f'data.json', "w") as file:
    json.dump(resulting_data, file)
