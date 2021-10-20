from typing import List
import requests
from bs4 import BeautifulSoup
from helper import random_headers

from http_requests import async_aiohttp_get_all


BASE_URL: str = 'https://eksisozluk.com/'
SEARCH_TAGS: List[str] = ['gain-medya--6770150']


def create_urls(current_page: str, page_count: str) -> List[str]:
    urls: List[str] = []
    start_page: int
    end_page: int

    try:
        start_page = int(current_page)
        end_page = int(page_count) + 1
    except ValueError:
        print('Conversion error')
        exit(0)

    if start_page >= end_page:
        print('single page content')
        return []

    for i in range(start_page + 1, end_page):
        urls.append(BASE_URL + SEARCH_TAGS[0] + '?p=' + str(i))

    return urls


def url_parser():
    pass


def main():
    # main page crawlign
    url: str = BASE_URL + SEARCH_TAGS[0]
    page = requests.get(url=url, headers=random_headers())
    soup = BeautifulSoup(page.content, 'html.parser')

    pager = soup.find('div', class_='pager')
    current_page: str = pager['data-currentpage']
    page_count: str = pager['data-pagecount']

    urls = create_urls(current_page, page_count)
    raw_page_list = async_aiohttp_get_all(urls)


if __name__ == "__main__":
    main()
