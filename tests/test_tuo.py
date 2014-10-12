from TwitterSearch import *

try: from urllib.parse import parse_qs, quote_plus, unquote # python3
except ImportError: from urlparse import parse_qs; from urllib import quote_plus, unquote #python2

import unittest
import random
import copy
import string
from datetime import date, timedelta

class TwitterUserOrderTest(unittest.TestCase):

    # some 'static' class variables
    _stduser = 'foo'

    def getCopy(self):
        """ Returns a deepcopy of the TSO object """

        return copy.deepcopy(self.__tuo)

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

        self.__tuo = TwitterUserOrder(self._stduser)

    ################ TESTS #########################

    def test_TUO_set_trim_user(self):
        """ Tests TwitterUserOrder.set_trim_user() """

        tuo = self.getCopy()
        values = [ True, False ]

        for value in values:
            tuo.set_trim_user(value)
            cor = '%s&trim_user=%s' % (self.__tuo.create_search_url, value)
            self.assertEqualQuery(tuo.create_search_url(), cor)

        values = [ -10, 10, 20.0, None, "", "foo" ]
        for value in values:
            try:
                tuo.set_trim_user(self.generateString())
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1008, "Wrong exception code")

    def test_TUO_set_include_rts(self):
        """ Tests TwitterUserOrder.set_include_rts() """

        tuo = self.getCopy()

        values = [ True, False ]
        for value in values:
            tuo.set_include_rts(value)
            cor = '%s&include_rts=%s' % (self.__tuo.create_search_url, value)
            self.assertEqualQuery(tuo.create_search_url(), cor)

        values = [ -10, 10, 20.0, None, "", "foo" ]
        for value in values:
            try:
                tuo.set_include_rts(self.generateString())
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1008, "Wrong exception code")


    def test_TUO_set_exclude_replies(self):
        """ Tests TwitterUserOrder.set_exclude_replies() """

        tuo = self.getCopy()

        values = [ True, False ]
        for value in values:
            tuo.set_exclude_replies(value)
            cor = '%s&exclude_replies=%s' % (self.__tuo.create_search_url, value)
            self.assertEqualQuery(tuo.create_search_url(), cor)

        values = [ -10, 10, 20.0, None, "", "foo" ]
        for value in values:
            try:
                tuo.set_exclude_replies(self.generateString())
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1008, "Wrong exception code")


    def test_TUO_set_contributor_details(self):
        """ Tests TwitterUserOrder.set_contributor_details() """

        tuo = self.getCopy()

        values = [ True, False ]
        for value in values:
            tuo.set_contributor_details(value)
            cor = '%s&contributor_details=%s' % (self.__tuo.create_search_url, value)
            self.assertEqualQuery(tuo.create_search_url(), cor)

        values = [ -10, 10, 20.0, None, "", "foo" ]
        for value in values:
            try:
                tuo.set_contributor_details(self.generateString())
                self.assertTrue(False, "Not raising exception for %s" % value)
            except TwitterSearchException as e:
                self.assertEqual(e.code, 1008, "Wrong exception code")

    def test_TUO_set_search_url(self):
        """ Tests TwitterUserOrder.set_search_url() """

        tuo1 = self.getCopy()
        tuo1.set_search_url('?contributor_details=true&exclude_replies=true&include_rts=false')

        tuo2 = TwitterUserOrder(self._stduser)
        tuo2.set_exclude_replies(True)
        tuo2.set_include_rts(False)
        tuo2.set_contributor_details(True)

        self.assertEqualQuery(tuo1.create_search_url(), tuo2.create_search_url(), "Query strings NOT equal")

    def test_TUO_contructuor(self):
        """ Tests __init__ method of TwitterUserOrder """

        value = 133.7

        from sys import hexversion

        if hexversion > 0x02060000: # everything newer than py2.6
            self.assertRaises(TwitterSearchException, TwitterUserOrder, value)
        else: # py2.6 <= fallback
            self.assertRaises(TwitterSearchException, TwitterUserOrder(value))