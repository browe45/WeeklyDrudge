"""
Package to hold classes for getting HTML page statistics
"""

import requests
import requests.exceptions
from collections import Counter
from bs4 import BeautifulSoup


class BulkHtmlRequester(object):
    """Gets HTML pages from the web and stores them in a list"""

    def __init__(self):
        self._content_list = list()

    def request_page(self, url):
        """
        Does HTML GET on a single URL and appends the main list
        :param url: URL string of html page
        :raises: HtmlStatException
        """
        try:
            self._content_list.append(requests.get(url).content)
        except requests.exceptions.MissingSchema as e:
            raise HtmlStatException(e)

    def request_pages(self, urls):
        """
        Requests a list of URLS
        :param urls: list of URL strings
        :raises: HtmlStatException
        """
        if len(urls) < 1:
            raise HtmlStatException("Empty list of URLs")

        for url in urls:
            self.request_page(url)

    def clear_contents(self):
        """
        Clears the contents of the list
        """
        del self._content_list
        self._content_list = list()


class HrefCounter(object):
    """Parses HTML content for HREF tags and keeps a counter"""

    def __init__(self):
        self._counter = Counter()

    def parse_contents(self, html_contents):
        """
        Search HTML contents for HREF tags and update counter
        :param html_contents: string of HTML contents
        """
        soup = BeautifulSoup(html_contents, 'html.parser')
        for link in soup.find_all('a'):
            self._counter[link.get('href')] += 1

    def parse_contents_list(self, html_contents_list):
        """
        Search list of HTML contents for HREF tags
        :param html_contents_list: list of HTML content strings
        """
        for html_contents in html_contents_list:
            self.parse_contents(html_contents)

    def top_ten(self):
        """
        Get top ten results
        :return: list of HREFs
        """
        return self._counter.most_common(10)

class HtmlStatException(Exception):
    """Exception class for this package"""