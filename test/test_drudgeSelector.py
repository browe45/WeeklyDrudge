from unittest import TestCase
from htmlstat.htmlstat import HtmlStatException
from htmlstat.drudge import DrudgeSelector
from datetime import date


class TestDrudgeSelector(TestCase):

    def test__check_date_order(self):
        s = DrudgeSelector(date(2015, 9, 1), date(2015, 9, 2))
        self.assertRaises(HtmlStatException, s._check_date_order, "", date(2015, 9, 2))
        self.assertRaises(HtmlStatException, s._check_date_order, date(2015, 9, 2), "")
        self.assertRaises(HtmlStatException, s._check_date_order, date(2015, 9, 3), date(2015, 9, 2))

    def test_query(self):

        # test invalid times and sample rates
        self.assertRaises(HtmlStatException, DrudgeSelector, None, date(2015, 9, 1))
        self.assertRaises(HtmlStatException, DrudgeSelector, "asdf", date(2015, 9, 1))
        self.assertRaises(HtmlStatException, DrudgeSelector, date(2015, 9, 1), None)
        self.assertRaises(HtmlStatException, DrudgeSelector, date(2015, 9, 1), "asdfad")
        self.assertRaises(HtmlStatException, DrudgeSelector, date(2015, 9, 1), date(2015, 9, 2), "asdf")
        self.assertRaises(HtmlStatException, DrudgeSelector, date(2015, 9, 1), date(2015, 9, 2), None)
        self.assertRaises(HtmlStatException, DrudgeSelector, date(2015, 9, 1), date(2015, 9, 2), 0)
        self.assertRaises(HtmlStatException, DrudgeSelector, date(2015, 9, 2), date(2015, 9, 1))

        d = DrudgeSelector(date(2015, 9, 1), date(2015, 9, 30), 2)
        self.assertRaises(HtmlStatException, d.query)

        #DrudgeSelector(date(1980, 9, 1), date(2015, 9, 2)).query()
        #DrudgeSelector(date(2015, 9, 1), date(2020, 9, 2)).query()

        # test site unavailable

        # test valid queries
        DrudgeSelector(date(2015, 9, 1), date(2015, 9, 2)).query()
