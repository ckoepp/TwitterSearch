from TwitterSearch import *


import unittest
import copy
import httpretty

class TwitterSearchOrder(unittest.TestCase):

    def createTS(self):
        """ Returns a default TwitterSearch instance """
        return TwitterSearch('aaabbb','cccddd','111222','333444', verify=False)

    def apiAnsweringMachine(self, filename):
        """ Generates faked API responses by returing content of a given file """
        for line in open(filename, 'r'):
            yield line

    def setUp(self):
        """ Constructor """
        self.auth_url = TwitterSearch._base_url + TwitterSearch._verify_url
        self.search_url = TwitterSearch._base_url + TwitterSearch._search_url



    ################ TESTS #########################

    @httpretty.activate
    def test_TS_authenticate(self):
        """ Tests TwitterSearch.authenticate() for valid logins """

        httpretty.register_uri(
                httpretty.GET, self.auth_url,
                body=self.apiAnsweringMachine('tests/mock-data/verify.log'),
                streaming=True,
                status=200,
                content_type='text/json' )

        ts = self.createTS()

        try:
            ts.authenticate(True)
            self.assertTrue(True)

        except TwitterSearchException as e:
            self.assertTrue(False, "An exception was raised: %s" % e)

    @httpretty.activate
    def test_TS_authenticate_fail(self):
        """ Tests TwitterSearch.authenticate() for invalid logins """

        httpretty.register_uri(
                httpretty.GET, self.auth_url,
                body=self.apiAnsweringMachine('tests/mock-data/verify-error.log'),
                streaming=True,
                status=401,
                content_type='text/json' )

        ts = self.createTS()

        try:
            ts.authenticate(True)
            self.assertTrue(False, "Exception should be raised instead")
        except TwitterSearchException as e:
            self.assertEqual(e.code, 401, "Exception code should be 401 but is %i" % e.code)
