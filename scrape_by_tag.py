import re
from typing import Any, Dict, List
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


def replace_html_tags(content: str) -> str:
    inside_html_tags = re.compile('<.*?>')

    new_string = re.sub(inside_html_tags, '', content)
    new_string = new_string.replace('\n', '')
    new_string = new_string.replace('\r', '')
    new_string = new_string.replace('\t', '')
    new_string = new_string.strip()

    return new_string


def comment_parser(comments: List[BeautifulSoup]):
    data_list = {}
    for comment in comments:
        content = comment.find('div', class_='content')
        content = replace_html_tags(content=content.text)

        author_id = comment.attrs['data-author-id']
        author_name = comment.attrs['data-author']
        comment_favorite_count = comment.attrs['data-favorite-count']

        if author_id in data_list.keys():
            data_list[author_id]['comments'].append(content)
            data_list[author_id]['favorite_count'] \
                .append(comment_favorite_count)
        else:
            data_list[author_id] = {
                'author_name': author_name,
                'comments': [content],
                'favorite_count': [comment_favorite_count]
            }
    print(data_list)


def url_parser(raw_content: List) -> List[BeautifulSoup]:
    retry_list: List[Dict[int: Any]] = []
    comments: List[BeautifulSoup] = []

    for index, page in enumerate(raw_content):
        soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
        container = soup.find('div', id='topic')

        if container is None:
            retry_list.append({index: page})
            continue
        # TODO: handle retry_list later
        comment_list = container.find('ul', id='entry-item-list')
        try:
            comment_list_item = comment_list.find_all('li')

            comments.extend(comment_list_item)
        except AttributeError:
            print('Has no entry-item-list')

    print(len(retry_list))
    if len(retry_list) > 0:
        exit(0)

    return comments


def main():
    # main page crawling
    url: str = BASE_URL + SEARCH_TAGS[0]
    page = requests.get(url=url, headers=random_headers())
    soup: BeautifulSoup = BeautifulSoup(page.content, 'html.parser')

    pager = soup.find('div', class_='pager')
    current_page: str = pager['data-currentpage']
    page_count: str = pager['data-pagecount']

    urls = create_urls(current_page, page_count)
    raw_page_list = async_aiohttp_get_all(urls)
    raw_page_list.insert(0, page.content)

    comments = url_parser(raw_page_list)
    comment_parser(comments)


if __name__ == "__main__":
    main()
