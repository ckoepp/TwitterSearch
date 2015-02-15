from TwitterSearch import *

import unittest
import httpretty

class TwitterSearchTest(unittest.TestCase):

    def createTSO(self):
        """ Returns a default TwitterSearchOrder instance """
        tso = TwitterSearchOrder()
        tso.set_keywords(['foo'])
        return tso

    def createTUO(self, username="foo"):
        """ Returns a default TwitterUserOrder instance """
        return TwitterUserOrder(username)

    def createTS(self):
        """ Returns a default TwitterSearch instance """
        return TwitterSearch('aaabbb','cccddd','111222','333444', verify=False)

    def apiAnsweringMachine(self, filename):
        """ Generates faked API responses by returing content of a given file """
        f = open(filename, 'r')
        for line in f:
            yield line
        f.close()

    def setUp(self):
        """ Constructor """
        self.auth_url = TwitterSearch._base_url + TwitterSearch._verify_url
        self.search_url = TwitterSearch._base_url + TwitterSearch._search_url
        self.lang_url = TwitterSearch._base_url + TwitterSearch._lang_url
        self.user_url = TwitterSearch._base_url + TwitterSearch._user_url


    ################ TESTS #########################

    @httpretty.activate
    def test_TS_set_supported_languages(self):
        """ Tests TwitterSearch.set_supported_languages() """

        httpretty.register_uri(
                httpretty.GET, self.lang_url,
                body=self.apiAnsweringMachine('tests/mock-data/lang.log'),
                streaming=True,
                status=200,
                content_type='text/json' )

        ts = self.createTS()
        tso = self.createTSO()

        try:
            ts.set_supported_languages(tso)
            self.assertEqual(tso.iso_6391.sort(), [ 'fi', 'da', 'pl', 'hu', 'fa', 'he' ].sort())
        except Exception as e:
            self.assertTrue(False, "An exception was raised: %s" % e)

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

    @httpretty.activate
    def test_TS_search_usertimeline_iterable(self):
        """ Tests TwitterSearch.search_tweets_iterable() and .get_statistics() by using TwitterUserOrder class """

        httpretty.register_uri(httpretty.GET, self.user_url,
                        responses=[
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/user/0.log')),
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/user/1.log')),

                            # add an empty page to mock the behavior of Twitter Timeline API
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/user/2.log')) 
                            ]
                        )

        expected_cnt = 390 # 200 in 0.log and 190 in 1.log (2.log is empty)
        pages = 3 # 0.log, 1.log and 2.log

        ts = self.createTS()
        tuo = self.createTUO()
        tweet_cnt = 0

        for tweet in ts.search_tweets_iterable(tuo):
            tweet_cnt += 1

        # test statistics
        stats = ts.get_statistics()
        self.assertEqual(stats[1], tweet_cnt, "Tweet counter is NOT working correctly (%i should be %i)" % (stats[1], tweet_cnt))
        self.assertEqual(stats[0], pages, "Query counter is NOT working correctly (%i should be %i)" % (stats[0], pages))

    @httpretty.activate
    def test_TS_search_tweets_iterable_callback(self):
        """ Tests TwitterSearch.search_tweets_iterable(callback) by using TwitterSearchOrder class """

        import sys
        if sys.version_info[0] < 3:
            self.assertTrue(True) # Dummy test for py2 doesn't have Mock class
            return

        httpretty.register_uri(httpretty.GET, self.search_url,
                        responses=[
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/0.log')),
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/1.log')),
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/2.log')),
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/3.log'))
                            ]
                        )

        pages = 4
        tso = self.createTSO()
        tso.set_count(4)
        ts = self.createTS()

        from unittest.mock import Mock

        mock = Mock()
        for tweet in ts.search_tweets_iterable(tso, callback=mock):
            mock.assert_called_with(ts)

        times = len(mock.call_args_list)
        self.assertEqual(pages, times, "Callback function was NOT called 4 times but %i times" % times)

    @httpretty.activate
    def test_TS_search_tweets_iterable(self):
        """ Tests TwitterSearch.search_tweets_iterable() and .get_statistics() by using TwitterSearchOrder class """

        httpretty.register_uri(httpretty.GET, self.search_url,
                        responses=[
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/0.log')),
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/1.log')),
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/2.log')),
                            httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/3.log'))
                            ]
                        )

        cnt = 4
        pages = 4 # 4 pages with 4*4-1 tweets in total
        tso = self.createTSO()
        tso.set_count(cnt)
        ts = self.createTS()

        tweet_cnt = 0
        for tweet in ts.search_tweets_iterable(tso):
            tweet_cnt += 1

        self.assertEqual( (cnt*4-1), tweet_cnt, "Wrong amount of tweets")

        # test statistics
        stats = ts.get_statistics()
        self.assertEqual(stats[1], tweet_cnt, "Tweet counter is NOT working correctly (%i should be %i)" % (stats[1], tweet_cnt))
        self.assertEqual(stats[0], pages, "Query counter is NOT working correctly (%i should be %i)" % (stats[0], pages))


    @httpretty.activate
    def test_TS_empty_results(self):
        """ Tests TwitterSearch.search_tweets_iterable() with empty results """

        httpretty.register_uri(httpretty.GET, self.search_url, 
                responses=[
                    httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/empty.log')),
                ])

        tso = self.createTSO()
        ts = self.createTS()
        for tweet in ts.search_tweets_iterable(tso):
            self.assertFalse(True, "There should be no tweets to be found")


    @httpretty.activate
    def test_TS_search_tweets(self):
        """ Tests TwitterSearch.search_tweets() """

        httpretty.register_uri(httpretty.GET, self.search_url,
                responses=[
                    httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/0.log')),
                    httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/1.log')),
                    httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/2.log')),
                    httpretty.Response(streaming=True, status=200, content_type='text/json', body=self.apiAnsweringMachine('tests/mock-data/search/3.log'))
                    ]
                )

        cnt = 4
        tso = self.createTSO()
        tso.set_count(cnt)
        ts = self.createTS()

        todo = True
        next_max_id = 0

        max_ids = []

        while(todo):
            max_ids.append(next_max_id)
            response = ts.search_tweets(tso)
            todo = len(response['content']['statuses']) == cnt
            for tweet in response['content']['statuses']:
                tweet_id = tweet['id']
                if (tweet_id < next_max_id) or (next_max_id == 0):
                     next_max_id = tweet_id
                     next_max_id -= 1
            tso.set_max_id(next_max_id)

        self.assertEqual(max_ids, [0, 355715848851300353, 355714667852726271, 355712782454358015], "Max ids NOT equal")


    def test_TS_string_output(self):
        """ Tests the string conversion of TwitterSearch """

        access_token = "foobar"
        ts = TwitterSearch('aaabbb','cccddd', access_token, '333444', verify=False)
        self.assertEqual( "<%s %s>" % (ts.__class__.__name__, access_token), "%s" % ts)


    def test_TS_methods_exceptions(self):
        """ Tests various TwitterSearch methods with invalid inputs/states """

        ts = self.createTS()
        with self.assertRaises(TwitterSearchException):
            ts.get_minimal_id()
            ts.send_search(101)
            ts.search_tweets("foobar")
            ts.get_metadata()
            ts.get_tweets()
            ts.get_amount_of_tweets()
            ts.set_supported_languages("joe.doe")

    def test_TS_minimal_id(self):
        """ Tests TwitterSearch.get_minimal_id method without request done """

        ts = self.createTS()
        self.assertRaises(TwitterSearchException, ts.get_minimal_id, )       

    def test_TS_proxy(self):
        """ Tests the proxy functionality of TwitterSearch class """

        # test constructor
        example_proxy = "some.proxy.com:1337"
        ts = TwitterSearch('aaabbb','cccddd','111222','333444', proxy=example_proxy, verify=False)
        self.assertEqual(ts.get_proxy(), example_proxy)

        # test manual setup
        example_proxy = "test.com:123"
        ts.set_proxy(example_proxy)
        self.assertEqual(ts.get_proxy(), example_proxy)

        try:
            ts.set_proxy(29.0)
            self.assertTrue(False, "Exception should be raised instead")
        except TwitterSearchException as e:
            self.assertEqual(e.code, 1009, "Exception code should be 401 but is %i" % e.code)

