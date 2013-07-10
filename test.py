from TwitterSearch import *

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

    def setUp(self):
        """ Constructor """

        self.__tso = TwitterSearchOrder()
        self.__tso.setKeywords( [ self._stdkeyword ] )

    ################ TESTS #########################

    def test_TSO_ResultType(self):
        """ Tests TwitterSearchOrder.setResultType() """

        tso = self.getCopy()
        correct_values = [ 'recent', 'mixed', 'popular' ]

        for value in correct_values:
            tso.setResultType(value)
            cor = '%s&result_type=%s' % (self.__tso.createSearchURL(), value)
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

        # wrong values
        try:
            tso.setResultType(self.generateString())
            self.assertTrue(False, "Not raising exception for %s" % value)
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1003, "Wrong exception code")

    def test_TSO_until(self):
        """ Tests TwitterSearchOrder.setUntil() """

        tso = self.getCopy()
        today = date.today()
        correct_values = [ today, today - timedelta(days=1), today - timedelta(days=10), today - timedelta(days=371) ]
        for value in correct_values:
            tso.setUntil(value)
            cor = '%s&until=%s' % (self.__tso.createSearchURL(), value.strftime('%Y-%m-%d'))
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

        # wrong values
        wrong_values = [ today + timedelta(days=1), '', [], {}, -1, 39.0, 31, 'foobar' ]
        for value in wrong_values:
            try:
                tso.setUntil(value)
                assertTrue(False, "Not raising exception for %s" % value.strfttime('%Y-%m-%d'))
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1007, "Wrong exception code")


    def test_TSO_maxID(self):
        """ Tests TwitterSearchOrder.setMaxID() """

        tso = self.getCopy()
        correct_values = [ self.generateInt(1,999999999) for x in range(0,10) ]

        for value in correct_values:
            tso.setMaxID(value)
            cor = '%s&max_id=%i' % (self.__tso.createSearchURL(), value)
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

        # wrong values
        wrong_values = [ -1, 1.0, '', [], {} ]
        for value in wrong_values:
            try:
                tso.setMaxID(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1004, "Wrong exception code")

    def test_TSO_sinceID(self):
        """ Tests TwitterSearchOrder.setSinceID() """

        tso = self.getCopy()
        correct_values = [ self.generateInt(1,999999999) for x in range(0,10) ]

        for value in correct_values:
            tso.setSinceID(value)
            cor = '%s&since_id=%i' % (self.__tso.createSearchURL(), value)
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

        # wrong values
        wrong_values = [-1, 1.0, '', [], {} ]
        for value in wrong_values:
            try:
                tso.setSinceID(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1004, "Wrong exception code")

    def test_TSO_geo(self):
        """ Tests TwitterSearchOrder.setGeocode() """

        tso = self.getCopy()
        cor_geo = [ 0.0, -12.331, 99.019, 12.33 ]
        for lat in cor_geo:
            is_km = bool(random.getrandbits(1))
            lon = random.choice(cor_geo)
            radius = self.generateInt(1,100)
            tso.setGeocode( lat, lon, radius, km=is_km)

            unit = ( 'km' if is_km else 'mi' )

            cor = '%s&geocode=%s,%s,%s%s' % (self.__tso.createSearchURL(), lat, lon, radius, unit)
            self.assertEqual(tso.createSearchURL(), cor)

        # wrong values
        wrong_values = [-1, 1.0, 101, '', [], {} ]
        for value in wrong_values:
            try:
                tso.setGeocode( value, value, self.generateInt(-200,-1), km=bool(random.getrandbits(1)))
                self.assertTrue(False, "Not raising exception for %s,%s,%" % value)
            except TwitterSearchException as e:
                self.assertTrue((e.code == 1004 or e.code == 1005), "Wrong exception code")


    def test_TSO_count(self):
        """ Tests TwitterSearchOrder.setCount() """

        tso = self.getCopy()
        correct_values = [ self.generateInt(minimum=1,maximum=100) for x in range(0,10) ]

        for value in correct_values:
            tso.setCount(value)
            cor = '%s%i' % (self.__tso.createSearchURL()[0:-3], value)
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

        # wrong values
        wrong_values = [ -1, 1.0, 101, '', [], {} ]
        for value in wrong_values:
            try:
                tso.setCount(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1004, "Wrong exception code")

    def test_TSO_callback(self):
        """ Tests TwitterSearchOrder.setCallback() """

        tso = self.getCopy()
        correct_values = [ self.generateString() for x in range(0,10) ]

        for value in correct_values:
            tso.setCallback(value)
            cor = '%s&callback=%s' % (self.__tso.createSearchURL(), value)
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

            # wrong values
            wrong_values = [ '', 1, 1.0, [], {} ]
            for value in wrong_values:
                try:
                    tso.setCallback(value)
                    self.assertTrue(False, "Not raising exception for %s" % value)
                except TwitterSearchException as e:
                    self.assertEqual(e.code, 1006, "Wrong exception code")

    def test_TSO_language(self):
        """ Tests TwitterSearchOrder.setLanguage() """

        tso = self.getCopy()
        for value in TwitterSearchOrder.iso_6391:
            tso.setLanguage(value)
            cor = '%s&lang=%s' % (self.__tso.createSearchURL(), value)
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

        # wrong values
        wrong_values = [ '', 'dee', 'q', 'xz', 32, 1.0, [], {} ]
        for value in wrong_values:
            try:
                tso.setLanguage(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1002, "Wrong exception code")

    def test_TSO_locale(self):
        """ Tests TwitterSearchOrder.setLanguage() """

        tso = self.getCopy()
        for value in TwitterSearchOrder.iso_6391:
            tso.setLocale(value)
            cor = '%s&locale=%s' % (self.__tso.createSearchURL(), value)
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

            # wrong values
            wrong_values = [ '', 'dee', 'q', 'xz', 32, 1.0, [], {} ]
            for value in wrong_values:
                try:
                    tso.setLocale(value)
                    self.assertTrue(False, "Not raising exception for %s" % value)
                except TwitterSearchException as e:
                    self.assertEqual(e.code, 1002, "Wrong exception code")

    def test_TSO_inclEntities(self):
        """ Tests TwitterSearchOrder.setIncludeEntities() """

        tso = self.getCopy()
        correct_values = [ True, False ]
        for value in correct_values:
            tso.setIncludeEntities(value)
            cor = '%s&include_entities=%s' % (self.__tso.createSearchURL(), bool(value))
            self.assertEqual(tso.createSearchURL(), cor, "Wrong URL")

        # wrong values
        wrong_values = [ '', 3.0, 3, -1, 2, [], {} ]
        for value in wrong_values:
            try:
                tso.setIncludeEntities(value)
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                    self.assertEqual(e.code, 1008)

    def test_TSO_keywords(self):
        """ Tests TwitterSearchOrder.setKeywords() and .addKeyword() """

        tso = self.getCopy()
        tso.setKeywords([ 'foo', 'bar' ])
        self.assertEqual(tso.createSearchURL()[0:10], '?q=foo+bar', "Keywords are NOT equal")

        tso.addKeyword(['one', 'two'])
        self.assertEqual(tso.createSearchURL()[0:18], '?q=foo+bar+one+two', "Keywords are NOT equal")

        tso.addKeyword('test')
        self.assertEqual(tso.createSearchURL()[0:23], '?q=foo+bar+one+two+test', "Keywords are NOT equal")

        tso.setKeywords(['test'])
        self.assertEqual(tso.createSearchURL()[0:7], '?q=test', "Keywords are NOT equal")

        # wrong values
        tso2 = TwitterSearchOrder()
        try:
            tso2.createSearchURL()
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1015, "Wrong exception code")


    def test_TSO_setURL(self):
        """ Tests TwitterSearchOrder.setSearchURL() """

        tso1 = self.getCopy()
        tso1.setSearchURL('?q=test1+test2&count=77&until=2013-07-10&locale=en')

        tso2 = TwitterSearchOrder()
        tso2.setKeywords([ 'test1', 'test2' ])
        tso2.setCount(77)
        tso2.setUntil(date(2013,7,10))
        tso2.setLocale('en')

        self.assertEqual(tso1.createSearchURL(), tso2.createSearchURL(), "Query strings NOT equal")

