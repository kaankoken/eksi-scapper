from asyncio.tasks import sleep
from typing import Any, Coroutine, List, Tuple
from aiohttp.client import ClientSession
import asyncio
import aiohttp
from requests.api import get


async def fetch(site) -> Coroutine[Any, Any, bytes]:
    async with aiohttp.ClientSession() as session, \
            session.get(site) as response:
        return await response.read()


async def get_all_req(loop, urls: List[str]) -> List:
    tasks = []
    for url in urls:
        await sleep(0.3)
        task = loop.create_task(fetch(url))
        tasks.append(task)
    return await asyncio.gather(*tasks)


def async_aiohttp_get_all(urls: List[str]) -> List:
    '''
        performs asynchronous get requests
    '''
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_all_req(loop, urls))
