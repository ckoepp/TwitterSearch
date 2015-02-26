from TwitterSearch import *

try: from urllib.parse import parse_qs, quote_plus, unquote # python3
except ImportError: from urlparse import parse_qs; from urllib import quote_plus, unquote #python2

import unittest
import random
import copy
import string
from datetime import date, timedelta

class TwitterSearchOrderTest(unittest.TestCase):

    # some 'static' class variables
    _stdkeyword = 'foo'

    def getCopy(self):
        """ Returns a deepcopy of the TSO object """

        return copy.deepcopy(self.__tso)

    def generateString(self, size=6, chars=string.ascii_uppercase + string.digits):
        """ Generates random strings """

        return ''.join(random.choice(chars) for x in range(size))

    def generateInt(self, minimum=0, maximum=100):
        """ Generates random integers """

        return random.randint(minimum,maximum)

    def assertEqualQuery(self, *args):
        """ Creates dicts out of given strings and compares those dicts """

        d = []
        for arg in args:
            d += parse_qs(arg)

        # it's slower if assertsEqual is done when x == y as to avoid this case
        (self.assertEqual(x,y,'Query strings do NOT match') for x in d for y in d)

    def setUp(self):
        """ Constructor """

        self.__tso = TwitterSearchOrder()
        self.__tso.set_keywords( [ self._stdkeyword ] )

    ################ TESTS #########################

    def test_TSO_result_type(self):
        """ Tests TwitterSearchOrder.set_result_type() """

        tso = self.getCopy()
        correct_values = [ 'recent', 'mixed', 'popular' ]

        for value in correct_values:
            tso.set_result_type(value)
            cor = '%s&result_type=%s' % (self.__tso.create_search_url(), value)
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        try:
            tso.set_result_type(self.generateString())
            self.assertTrue(False, "Not raising exception for %s" % value)
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1003, "Wrong exception code")

    def test_TSO_until(self):
        """ Tests TwitterSearchOrder.set_until() """

        tso = self.getCopy()
        today = date.today()
        correct_values = [ today, today - timedelta(days=1), today - timedelta(days=10), today - timedelta(days=371) ]
        for value in correct_values:
            tso.set_until(value)
            cor = '%s&until=%s' % (self.__tso.create_search_url(), value.strftime('%Y-%m-%d'))
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        wrong_values = [ today + timedelta(days=1), '', [], {}, -1, 39.0, 31, 'foobar' ]
        for value in wrong_values:
            try:
                tso.set_until(value)
                assertTrue(False, "Not raising exception for %s" % value.strfttime('%Y-%m-%d'))
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1007, "Wrong exception code")

    def test_TSO_search_encoding(self):
        """ Tests the url encoding of TwitterSearchOrder.create_search_url() """

        test_cases = [ 'test(', '[test' , 'foo$bar','plain', '==', '=%!' ]

        for value in test_cases:
            tso = TwitterSearchOrder()
            tso.add_keyword(value)
            cor = '?q=%s&count=%s' % (quote_plus(value),tso._max_count)
            self.assertEqualQuery(tso.create_search_url(), cor)


    def test_TSO_maxID(self):
        """ Tests TwitterSearchOrder.set_max_id() """

        tso = self.getCopy()
        correct_values = [ self.generateInt(1,999999999) for x in range(0,10) ]

        for value in correct_values:
            tso.set_max_id(value)
            cor = '%s&max_id=%i' % (self.__tso.create_search_url(), value)
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        wrong_values = [ -1, 1.0, '', [], {} ]
        for value in wrong_values:
            try:
                tso.set_max_id(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1004, "Wrong exception code")

    def test_TSO_sinceID(self):
        """ Tests TwitterSearchOrder.set_since_id() """

        tso = self.getCopy()
        correct_values = [ self.generateInt(1,999999999) for x in range(0,10) ]

        for value in correct_values:
            tso.set_since_id(value)
            cor = '%s&since_id=%i' % (self.__tso.create_search_url(), value)
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        wrong_values = [-1, 1.0, '', [], {} ]
        for value in wrong_values:
            try:
                tso.set_since_id(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1004, "Wrong exception code")

    def test_TSO_geo(self):
        """ Tests TwitterSearchOrder.set_geocode() """

        tso = self.getCopy()
        cor_geo = [ 0.0, -12.331, 99.019, 12.33 ]
        for lat in cor_geo:
            is_km = bool(random.getrandbits(1))
            lon = random.choice(cor_geo)
            radius = self.generateInt(1,100)
            tso.set_geocode( lat, lon, radius, imperial_metric=is_km)

            unit = ( 'km' if is_km else 'mi' )

            cor = '%s&geocode=%s,%s,%s%s' % (self.__tso.create_search_url(), lat, lon, radius, unit)
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        wrong_values = [-1, 1.0, 101, '', [], {} ]
        for value in wrong_values:
            try:
                radius = self.generateInt(-200,-1)
                unit = bool(random.getrandbits(1))
                tso.set_geocode( value, value, radius, imperial_metric=unit)
                self.assertTrue(False, "Not raising exception for lat %s, lon %s, radius %s and metric %s" % (value,value,radius,unit))
            except TwitterSearchException as e:
                self.assertTrue((e.code == 1004 or e.code == 1005), "Wrong exception code")

        try:
            tso.set_geocode(2.0,1.0,10, imperial_metric='foo')
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1005, 'Wrong exception code')

        try:
           tso.set_geocode('foo','bar',10)
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1004, 'Wrong exception code')
 
    def test_TSO_count(self):
        """ Tests TwitterSearchOrder.set_count() """

        tso = self.getCopy()
        correct_values = [ self.generateInt(minimum=1,maximum=100) for x in range(0,10) ]

        for value in correct_values:
            tso.set_count(value)
            cor = '%s%i' % (self.__tso.create_search_url()[0:-3], value)
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        wrong_values = [ -1, 1.0, 101, '', [], {} ]
        for value in wrong_values:
            try:
                tso.set_count(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1004, "Wrong exception code")

    def test_TSO_callback(self):
        """ Tests TwitterSearchOrder.set_callback() """

        tso = self.getCopy()
        correct_values = [ self.generateString() for x in range(0,10) ]

        for value in correct_values:
            tso.set_callback(value)
            cor = '%s&callback=%s' % (self.__tso.create_search_url(), value)
            self.assertEqualQuery(tso.create_search_url(), cor)

            # wrong values
            wrong_values = [ '', 1, 1.0, [], {} ]
            for value in wrong_values:
                try:
                    tso.set_callback(value)
                    self.assertTrue(False, "Not raising exception for %s" % value)
                except TwitterSearchException as e:
                    self.assertEqual(e.code, 1006, "Wrong exception code")

    def test_TSO_language(self):
        """ Tests TwitterSearchOrder.set_language() """

        tso = self.getCopy()
        for value in TwitterSearchOrder.iso_6391:
            tso.set_language(value)
            cor = '%s&lang=%s' % (self.__tso.create_search_url(), value)
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        wrong_values = [ '', 'dee', 'q', 'xz', 32, 1.0, [], {} ]
        for value in wrong_values:
            try:
                tso.set_language(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1002, "Wrong exception code")

    def test_TSO_locale(self):
        """ Tests TwitterSearchOrder.set_language() """

        tso = self.getCopy()
        for value in TwitterSearchOrder.iso_6391:
            tso.set_locale(value)
            cor = '%s&locale=%s' % (self.__tso.create_search_url(), value)
            self.assertEqualQuery(tso.create_search_url(), cor)

            # wrong values
            wrong_values = [ '', 'dee', 'q', 'xz', 32, 1.0, [], {} ]
            for value in wrong_values:
                try:
                    tso.set_locale(value)
                    self.assertTrue(False, "Not raising exception for %s" % value)
                except TwitterSearchException as e:
                    self.assertEqual(e.code, 1002, "Wrong exception code")

    def test_TSO_inclEntities(self):
        """ Tests TwitterSearchOrder.set_include_entities() """

        tso = self.getCopy()
        correct_values = [ True, False ]
        for value in correct_values:
            tso.set_include_entities(value)
            cor = '%s&include_entities=%s' % (self.__tso.create_search_url(), bool(value))
            self.assertEqualQuery(tso.create_search_url(), cor)

        # wrong values
        wrong_values = [ '', 3.0, 3, -1, 2, [], {} ]
        for value in wrong_values:
            try:
                tso.set_include_entities(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                    self.assertEqual(e.code, 1008)

    def test_TSO_keywords(self):
        """ Tests TwitterSearchOrder.set_keywords() and .add_keyword() """

        tso = self.getCopy()
        tso.set_keywords([ 'foo', 'bar' ])
        self.assertEqual(tso.create_search_url()[0:10], '?q=foo+bar', "Keywords are NOT equal")

        tso.add_keyword(['one', 'two'])
        self.assertEqual(tso.create_search_url()[0:18], '?q=foo+bar+one+two', "Keywords are NOT equal")

        tso.add_keyword('test')
        self.assertEqual(tso.create_search_url()[0:23], '?q=foo+bar+one+two+test', "Keywords are NOT equal")

        tso.set_keywords(['test'])
        self.assertEqual(tso.create_search_url()[0:7], '?q=test', "Keywords are NOT equal")

        # space keywords
        space_test = "James Bond"
        test_against = "%22" + space_test.replace(" ","+") + "%22"
        tso.add_keyword(space_test)
        self.assertTrue(test_against in tso.create_search_url())
        tso.set_keywords([space_test])
        self.assertTrue(test_against in tso.create_search_url())

        # wrong values
        try:
            tso.add_keyword({ 'foo' : 'bar' })
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1000, "Wrong exception code")

        try:
            tso.set_keywords({ 'other' : 'stuff'})
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1001, "Wrong exception code")

        tso2 = TwitterSearchOrder()
        try:
            tso2.create_search_url()
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1015, "Wrong exception code")

    def test_TSO_add_keyword_OR(self):
        """" Tests TwitterSearchOrder.add_keyword(or_operator) """

        tso = self.getCopy()
        keywords = ("bob","alice")
        tso.add_keyword(keywords, or_operator=True)
        self.assertTrue("+or+".join(keywords) in tso.create_search_url().lower())

    def test_TSO_set_keywords_OR(self):
        """" Tests TwitterSearchOrder.set_keywords(or_operator) """

        tso = self.getCopy()
        keywords = ("bob","alice")
        tso.set_keywords(keywords, or_operator=True)
        self.assertTrue("+or+".join(keywords) in tso.create_search_url().lower())

    def test_TSO_filters(self):
        """ Tests TwitterSearchOrder advanced filtering methods """

        tso = self.getCopy()

        # source filter
        source = "nyancat"
        self.assertTrue(tso.source_filter is None) # default
        tso.set_source_filter(source)
        self.assertEqual(tso.source_filter, source)
        self.assertTrue("source%3a" + source in tso.create_search_url().lower())
        tso.remove_source_filter()
        self.assertTrue(tso.source_filter is None)

        # check for exception when inserting invalid values
        for obj in ([], {}, None, 2, 37.1, ""):
            with self.assertRaises(TwitterSearchException):
                tso.set_source_filter(obj)

        # link filter
        self.assertFalse(tso.link_filter) # default
        tso.set_link_filter()
        self.assertTrue(tso.link_filter)
        self.assertTrue("filter%3alinks" in tso.create_search_url().lower())
        tso.remove_link_filter()
        self.assertFalse(tso.link_filter)

        # question filter
        self.assertFalse(tso.question_filter) # default
        tso.set_question_filter()
        self.assertTrue(tso.question_filter)
        self.assertTrue("%3f" in tso.create_search_url().lower())
        tso.remove_question_filter()
        self.assertFalse(tso.question_filter)

        # negative attitude filter
        self.assertTrue(tso.attitude_filter is None) # default
        tso.set_negative_attitude_filter()
        self.assertFalse(tso.attitude_filter)
        self.assertTrue("%3a%28" in tso.create_search_url().lower())
        tso.remove_attitude_filter()
        self.assertTrue(tso.attitude_filter is None)

        # positive attitude filter
        tso.set_positive_attitude_filter()
        self.assertTrue(tso.attitude_filter)
        self.assertTrue("%3a%29" in tso.create_search_url().lower())
        tso.remove_attitude_filter()
        self.assertTrue(tso.attitude_filter is None)

    def test_TSO_setURL(self):
        """ Tests TwitterSearchOrder.set_search_url() """

        tso1 = self.getCopy()
        tso1.set_search_url('?q=test1+test2&count=77&until=2013-07-10&locale=en')

        # testing filter settings (off)
        self.assertFalse(tso1.question_filter)
        self.assertFalse(tso1.link_filter)
        self.assertTrue(tso1.source_filter is None)
        self.assertTrue(tso1.attitude_filter is None)

        tso2 = TwitterSearchOrder()
        tso2.set_keywords([ 'test1', 'test2' ])
        tso2.set_count(77)
        tso2.set_until(date(2013,7,10))
        tso2.set_locale('en')

        self.assertEqualQuery(tso1.create_search_url(), tso2.create_search_url(), "Query strings NOT equal")

        source = "alice"
        tso3 = self.getCopy()
        tso3.set_search_url('?q=foobar+%3A%29+%3F+filter%3Alinks+source%3A' + source)

        # testing filter settings (on)
        self.assertTrue(tso3.attitude_filter)
        self.assertTrue(tso3.question_filter)
        self.assertTrue(tso3.link_filter)
        self.assertEqual(tso3.source_filter, source)

        tso4 = TwitterSearchOrder()
        tso4.set_question_filter()
        tso4.set_positive_attitude_filter()
        tso4.set_link_filter()
        tso4.set_source_filter(source)
        tso4.add_keyword("foobar")
        self.assertEqualQuery(tso3.create_search_url(), tso4.create_search_url(), "Query strings NOT equal")

    def test_TO_exceptions(self):
        """ Tests unimplemented TwitterOrder functions aiming for exceptions """

        value = "foo"
        exc_class = NotImplementedError
        to = TwitterOrder()
        with self.assertRaises(exc_class):
            to.set_search_url(value)
            to.create_search_url()

