from typing import Any, Coroutine, List, Tuple
from aiohttp.client import ClientSession
import asyncio
import aiohttp

from helper import random_headers


async def fetch(url, session: ClientSession) -> Coroutine[Any, Any, bytes]:
    """
    asynchronous get request
    """
    async with session.get(url) as response:
        return await response.read()


async def fetch_many(loop, urls) -> Coroutine[Any, Any, Tuple]:
    '''
        many asynchronous get requests, gathered
    '''
    async with aiohttp.ClientSession(headers=random_headers()) as session:
        tasks = [loop.create_task(fetch(url, session)) for url in urls]
        return await asyncio.gather(*tasks)


def async_aiohttp_get_all(urls) -> List:
    '''
        performs asynchronous get requests
    '''
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetch_many(loop, urls))
