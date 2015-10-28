"""Package to hold URL queries for DrudgeReport"""

import htmlstat
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
import re


class DrudgeSelector(object):
    """Returns sets of URL samples"""

    def __init__(self, begin_date, end_date, samples=10):
        self._begin_date = None
        self._end_date = None
        self._samples = None

        self.begin_date = begin_date
        self.end_date = end_date
        self.samples = samples

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        if value is None:
            raise htmlstat.HtmlStatException("Sample must have a value: {0}".format(value))
        elif not isinstance(value, int):
            raise htmlstat.HtmlStatException("Invalid integer for sample: {0}".format(value))
        elif value < 1:
            raise htmlstat.HtmlStatException("Invalid value for sample: {0}".format(value))
        self._samples = value

    @property
    def begin_date(self):
        return self._begin_date

    @begin_date.setter
    def begin_date(self, value):
        if value is None:
            raise htmlstat.HtmlStatException("Begin date must have a value: {0}".format(value))
        elif not isinstance(value, date):
            raise htmlstat.HtmlStatException("Invalid begin date: {0}".format(value))
        self._check_date_order(value, self.end_date)
        self._begin_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        if value is None:
            raise htmlstat.HtmlStatException("End date must have a value: {0}".format(value))
        elif not isinstance(value, date):
            raise htmlstat.HtmlStatException("Invalid end date: {0}".format(value))
        self._check_date_order(self.begin_date, value)
        self._end_date = value

    @staticmethod
    def _check_date_order(begin_date, end_date):
        """
        Checks that the dates are ordered correctly
        :param begin_date: datetime.date for begin date
        :param end_date: datetime.date for end date
        :raises: HtmlStatException
        """
        if begin_date is None:
            if not isinstance(end_date, date):
                raise htmlstat.HtmlStatException("Invalid end date type to check order")
            return

        if end_date is None:
            if not isinstance(begin_date, date):
                raise htmlstat.HtmlStatException("Invalid begin date type to check order")
            return

        if not isinstance(begin_date, date) or not isinstance(end_date, date):
            raise htmlstat.HtmlStatException("Invalid date type to check order")
        elif begin_date > end_date:
            raise htmlstat.HtmlStatException("Incorrect date ordering")

    def query(self):
        """
        Run queries to get content of past Drudge Report pages
        :return: list of HTML content strings
        :raises: HtmlStatException
        """

        delta = self.end_date - self.begin_date
        samples_per_day, remainder = divmod(self.samples, delta.days)
        if samples_per_day < 1:
            raise htmlstat.HtmlStatException("Not enough samples for time frame")

        results_list = list()
        for i in range(0, delta.days):
            samples = samples_per_day + 1 if i < remainder else samples_per_day
            offset = timedelta(i)
            self._daily_query(self.begin_date + offset, samples, results_list)

        return results_list

    def _daily_query(self, query_date, samples, results_list):
        """
        Get URLs for a sample of pages in a single day
        :param query_date: date of pages
        :param samples: number of pages to get
        :param results_list: list of HTML content for pages retrieved
        """
        url = self._build_archive_url(query_date)
        r = requests.get(url)
        ptn = re.compile("{0}/{1:0>2}/{2:0>2}".format(query_date.year, query_date.month, query_date.day))
        href_list = self._sample_hrefs(r.content, samples, ptn)
        for href in href_list:
            r = requests.get(href)
            results_list.append(r.content)

    # Constant string used for archive URL
    ARCHIVE_URL = "http://www.drudgereportarchives.com/data/{0}/{1:0>2}/{2:0>2}/index.htm"

    def _build_archive_url(self, query_date):
        """
        Get a URL for the archive page containing list of pages for each day
        :param query_date: date of pages
        :return: URL string
        """
        return self.ARCHIVE_URL.format(query_date.year, query_date.month, query_date.day)

    def _sample_hrefs(self, html_content, samples, ptn):
        """
        Returns a list of URLs of pages to query
        :param html_content: content of the archive page
        :param samples: number of URLs to return
        :param ptn: pattern to match the URLs
        :return: list of URL strings
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        i = 0
        href_list = list()
        for link in soup.find_all('a'):
            if ptn.search(link.get('href')) is None:
                continue
            href_list.append(link.get('href'))
            i += 1
            if i >= samples:
                break
        return href_list
