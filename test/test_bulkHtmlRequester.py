from unittest import TestCase
import htmlstat.htmlstat


class TestBulkHtmlRequester(TestCase):
    def test_request_page(self):
        # test invalid url
        r = htmlstat.htmlstat.BulkHtmlRequester()
        self.assertRaises(htmlstat.htmlstat.HtmlStatException, r.request_page, "")
        self.assertTrue(len(r._content_list) < 1)
        self.assertRaises(htmlstat.htmlstat.HtmlStatException, r.request_page, "asdfadf")
        self.assertTrue(len(r._content_list) < 1)

        # test valid url
        r.request_page("http://www.google.com")
        self.assertTrue(len(r._content_list) == 1)
        self.assertTrue(len(r._content_list[0]) > 0)

    def test_request_pages(self):
        # test empty list
        r = htmlstat.htmlstat.BulkHtmlRequester()
        self.assertRaises(htmlstat.htmlstat.HtmlStatException, r.request_pages, [])

        # test list of invalids
        self.assertRaises(htmlstat.htmlstat.HtmlStatException, r.request_pages, ["", "asdfasf"])

        # test valid list
        r.request_pages(["http://www.google.com", "http://www.yahoo.com"])
        self.assertTrue(len(r._content_list) == 2)

    def test_clear_contents(self):
        # test that contents are initially clear
        r = htmlstat.htmlstat.BulkHtmlRequester()
        self.assertTrue(len(r._content_list) < 1)
        r.clear_contents()
        self.assertTrue(len(r._content_list) < 1)

        # request page and assert not clear
        r.request_page("http://www.google.com")
        self.assertTrue(len(r._content_list) == 1)

        # run clear
        r.clear_contents()
        self.assertTrue(len(r._content_list) < 1)
