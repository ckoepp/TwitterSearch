# -*- coding: utf-8 -*-

import requests
from requests_oauthlib import OAuth1
from .TwitterSearchException import TwitterSearchException
from .TwitterOrder import TwitterOrder
from .TwitterSearchOrder import TwitterSearchOrder
from .TwitterUserOrder import TwitterUserOrder
from .utils import py3k

try: from urllib.parse import parse_qs # python3
except ImportError: from urlparse import parse_qs # python2

# determine max int value
try: from sys import maxint # python2
except ImportError: from sys import maxsize as maxint # python3

class TwitterSearch(object):
    """
    This class actually performs the calls to the Twitter Search API (v1.1 only).

    It is configured using an instance of TwitterSearchOrder and valid Twitter credentials.
    """

    _base_url = 'https://api.twitter.com/1.1/'
    _verify_url = 'account/verify_credentials.json'
    _search_url = 'search/tweets.json'
    _lang_url = 'help/languages.json'
    _user_url = 'statuses/user_timeline.json'

    # see https://dev.twitter.com/docs/error-codes-responses
    exceptions = {
                     400 : 'Bad Request: The request was invalid',
                     401 : 'Unauthorized: Authentication credentials were missing or incorrect',
                     403 : 'Forbidden: The request is understood, but it has been refused or access is not allowed',
                     404 : 'Not Found: The URI requested is invalid or the resource requested does not exists',
                     406 : 'Not Acceptable: Invalid format is specified in the request',
                     410 : 'Gone: This resource is gone',
                     420 : 'Enhance Your Calm:  You are being rate limited',
                     422 : 'Unprocessable Entity: Image unable to be processed',
                     429 : 'Too Many Requests: Request cannot be served due to the application\'s rate limit having been exhausted for the resource',
                     500 : 'Internal Server Error: Something is broken',
                     502 : 'Bad Gateway: Twitter is down or being upgraded',
                     503 : 'Service Unavailable: The Twitter servers are up, but overloaded with requests',
                     504 : 'Gateway timeout: The request couldn\'t be serviced due to some failure within our stack',
                 }

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, **attr):

        # app
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

        # user
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret

        # init internal variables
        self.__response = {}
        self.__nextMaxID = maxint
        self.__next_tweet = 0

        if "proxy" in attr:
            self.set_proxy(attr["proxy"])
        else:
            self.__proxy = None

        # statistics
        self.__statistics = { 'queries' : 0, 'tweets' : 0 }

        # verify
        self.authenticate( attr["verify"] if "verify" in attr else True )

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.__access_token)

    def set_proxy(self, proxy):
        """ Sets a given dict as proxy handler """
        if isinstance(proxy, str if py3k else basestring):
            self.__proxy = proxy
        else:
            raise TwitterSearchException(1009)

    def get_proxy(self):
        """ Returns the current proxy url or None if no proxy is set """
        return self.__proxy

    def authenticate(self, verify=True):
        """ Creates internal oauth handler needed for queries to Twitter and verifies credentials if needed """
        self.__oauth = OAuth1(self.__consumer_key,
            client_secret = self.__consumer_secret,
            resource_owner_key = self.__access_token,
            resource_owner_secret = self.__access_token_secret )

        if verify:
            r = requests.get(self._base_url + self._verify_url, auth=self.__oauth, proxies={"https":self.__proxy})
            self.check_http_status(r.status_code)

    def check_http_status(self, http_status):
        """ Checks a given http_status and returns an exception in case wrong status """
        if http_status in self.exceptions:
            raise TwitterSearchException(http_status, self.exceptions[http_status])

    def search_tweets_iterable(self, order):
        """ Returns itself. Is called when using an instance of this class as iterable """
        self.search_tweets(order)
        return self

    def get_minimal_id(self):
        """ Returns the minimal Tweet ID of the current response """
        if not self.__response:
            raise TwitterSearchException(1013)

        return min(
                self.__response['content']['statuses'] if self.__order_is_search else self.__response['content'],
                key=lambda i: i['id']
                )['id'] - 1


    def send_search(self, url):
        """ Sends a given query string to the Twitter Search API, stores results interally and validates returned HTTP status code """
        if not isinstance(url, str if py3k else basestring):
            raise TwitterSearchException(1009)

        endpoint = self._base_url + (self._search_url if self.__order_is_search else self._user_url)

        r = requests.get(endpoint + url, auth=self.__oauth, proxies={"https":self.__proxy})
        self.__response['meta'] = r.headers

        self.check_http_status(r.status_code)

        self.__response['content'] = r.json()

        # update statistics if everything worked fine so far
        seen_tweets = self.get_amount_of_tweets()
        self.__statistics['queries'] += 1
        self.__statistics['tweets'] += seen_tweets

        # if we've seen the correct amount of tweets there may be some more
        # using IDs to request more results - former versions used page parameter
        # see https://dev.twitter.com/docs/working-with-timelines
        if url[0] == '?': # a leading ? char does "confuse" parse_qs()
            url = url[1:]
        given_count = int(parse_qs(url)['count'][0])

        # Search API does have valid count values
        if self.__order_is_search and seen_tweets == given_count:
            self.__next_max_id = self.get_minimal_id()

        # Timelines doesn't have valid count values
        # see: https://dev.twitter.com/docs/faq - section: "How do I properly navigate a timeline?"
        # ToDo: see wether this works (implement test case with zero statuses!)
        elif not self.__order_is_search and len(self.__response['content']) > 0:
            self.__next_max_id = self.get_minimal_id()

        else: # we got less tweets than requested -> no more results in API
            self.__next_max_id = None

        return self.__response['meta'], self.__response['content']

    def search_tweets(self, order):
        """ Creates an query string through a given TwitterSearchOrder instance and takes care that it is send to the Twitter API. Returns unmodified response """
        if isinstance(order, TwitterUserOrder):
            self.__order_is_search = False
        elif isinstance(order, TwitterSearchOrder):
            self.__order_is_search = True
        else:
            raise TwitterSearchException(1018)

        self._start_url = order.create_search_url()
        self.send_search(self._start_url)
        return self.__response

    def search_next_results(self):
        """ Returns True if there are more results available within the Twitter Search API """
        if not self.__next_max_id:
            raise TwitterSearchException(1011)

        self.send_search("%s&max_id=%i" % (self._start_url, self.__next_max_id))
        return True

    def get_metadata(self):
        """ Returns all available meta data collected during last query """
        if not self.__response:
            raise TwitterSearchException(1012)
        return self.__response['meta']

    def get_tweets(self):
        """ Returns all available data from last query """
        if not self.__response:
           raise TwitterSearchException(1013)
        return self.__response['content']

    def get_statistics(self):
        """ Returns dict with statistical information about amount of queries and received tweets """
        return self.__statistics

    def get_amount_of_tweets(self):
        """ Returns current amount of tweets available within this instance """
        if not self.__response:
           raise TwitterSearchException(1013)
        return len(self.__response['content']['statuses']) if self.__order_is_search else len(self.__response['content'])


    def set_supported_languages(self, order):
        """ Loads currently supported languages from Twitter API and sets them in a given TwitterSearchOrder instance """
        if not isinstance(order, TwitterSearchOrder):
            raise TwitterSearchException(1010)

        r = requests.get(self._base_url + self._lang_url, auth=self.__oauth, proxies={"https":self.__proxy})
        self.__response['meta'] = r.headers
        self.check_http_status(r.status_code)
        self.__response['content'] = r.json()

        order.iso_6391 =  []
        for lang in self.__response['content']:
            order.iso_6391.append(lang['code'])

    # Iteration
    def __iter__(self):
        self.__next_tweet = 0
        return self

    def next(self):
        """ Python2 method, simply returns self.__next__() """
        return self.__next__()

    def __next__(self):
        if not self.__response:
            raise TwitterSearchException(1014)

        if self.__next_tweet < self.get_amount_of_tweets():
            self.__next_tweet += 1
            if self.__order_is_search:
                return self.__response['content']['statuses'][self.__next_tweet-1]
            else:
                return self.__response['content'][self.__next_tweet-1]

        try:
            self.search_next_results()
        except TwitterSearchException:
            raise StopIteration

        if self.get_amount_of_tweets() != 0:
            self.__next_tweet = 1
            if self.__order_is_search:
                return self.__response['content']['statuses'][self.__next_tweet-1]
            else:
                return self.__response['content'][self.__next_tweet-1]
        raise StopIteration
