# -*- coding: utf-8 -*-

import requests
from requests_oauthlib import OAuth1
from .TwitterSearchException import TwitterSearchException
from .TwitterOrder import TwitterOrder
from .TwitterSearchOrder import TwitterSearchOrder
from .TwitterUserOrder import TwitterUserOrder
from .utils import py3k


try:
    from urllib.parse import parse_qs  # python3
except ImportError:
    from urlparse import parse_qs  # python2

# determine max int value
try:
    from sys import maxint  # python2
except ImportError:
    from sys import maxsize as maxint  # python3


class TwitterSearch(object):
    """
    This class contains the actual functionality of this library. 
    It is responsible for correctly transmitting your data to the Twitter API 
    (v1.1 only) and returning the results to your program afterwards.
    It is configured using an implementation of :class:`TwitterOrder` 
    along with valid Twitter credentials. Currently two different
    implementations are usable: :class:`TwitterUserOrder` for retrieving the
    timeline of a certain user and :class:`TwitterSearchOrder` for accessing
    the Twitter Search API.

    The methods ``next()``, ``__next__()`` and ``__iter__()`` are used 
    during the iteration process. For more information about those 
    methods please consult the `official Python
    documentation
    <http://docs.python.org/2/library/stdtypes.html#iterator-types>`_.
    """

    _base_url = 'https://api.twitter.com/1.1/'
    _verify_url = 'account/verify_credentials.json'
    _search_url = 'search/tweets.json'
    _lang_url = 'help/languages.json'
    _user_url = 'statuses/user_timeline.json'

    # see https://dev.twitter.com/docs/error-codes-responses
    exceptions = {
        400: 'Bad Request: The request was invalid',
        401: ('Unauthorized: Authentication credentials ',
              ' were missing or incorrect'),
        403: ('Forbidden: The request is understood, but',
              'it has been refused or access is not allowed'),
        404: ('Not Found: The URI requested is invalid or',
              'the resource requested does not exists'),
        406: 'Not Acceptable: Invalid format is specified in the request',
        410: 'Gone: This resource is gone',
        420: 'Enhance Your Calm:  You are being rate limited',
        422: 'Unprocessable Entity: Image unable to be processed',
        429: ('Too Many Requests: Request cannot be served ',
              'due to the application\'s rate limit having ',
              'been exhausted for the resource'),
        500: 'Internal Server Error: Something is broken',
        502: 'Bad Gateway: Twitter is down or being upgraded',
        503: ('Service Unavailable: The Twitter servers ',
              'are up, but overloaded with requests'),
        504: ('Gateway timeout: The request couldn\'t ',
              'be serviced due to some failure within our stack'),
    }

    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret, **attr):
        """ Constructor

        :param consumer_key: Consumer key (app related)
        :param consumer_secret: Consumer consumer_secret (app related)
        :param access_token: Access token (user related)
        :param access_token_secret: Access token secret (user related)

        :param verify: A boolean variable to control verification of \
        access codes. Default value is ``True`` which \
        raises an instant exception when using invalid credentials.

        :param proxy: A string containing a HTTPS proxy \
        (e.g. ``my.proxy.com:8080``). Default value is ``None`` \
        which means that no proxy is used at all.
        """

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
        self.__statistics = [0,0]

        # callback
        self.__callback = None

        # verify
        if "verify" in attr:
            self.authenticate(attr["verify"])
        else:
            self.authenticate(True)

    def __repr__(self):
        """ Returns the class and its access token

        :returns: A string represenation of this \
        class containing the class name and the used access token
        """

        return '<%s %s>' % (self.__class__.__name__, self.__access_token)

    def set_proxy(self, proxy):
        """ Sets a HTTPS proxy to query the Twitter API

        :param proxy: A string of containing a HTTPS proxy \
        e.g. ``set_proxy("my.proxy.com:8080")``.
        :raises: TwitterSearchException
        """

        if isinstance(proxy, str if py3k else basestring):
            self.__proxy = proxy
        else:
            raise TwitterSearchException(1009)

    def get_proxy(self):
        """ Returns the current proxy url or None if no proxy is set

        :returns: A string containing the current HTTPS proxy \
        (e.g. ``my.proxy.com:8080``) or ``None`` is no proxy is used
        """

        return self.__proxy

    def authenticate(self, verify=True):
        """ Creates an authenticated and internal oauth2  handler needed for \
        queries to Twitter and verifies credentials if needed.  If ``verify`` \
        is true, it also checks if the user credentials are valid. \
        The **default** value is *True*

        :param verify: boolean variable to \
        directly check. Default value is ``True``
        """

        self.__oauth = OAuth1(self.__consumer_key,
                              client_secret=self.__consumer_secret,
                              resource_owner_key=self.__access_token,
                              resource_owner_secret=self.__access_token_secret)

        if verify:
            r = requests.get(self._base_url + self._verify_url,
                             auth=self.__oauth,
                             proxies={"https": self.__proxy})
            self.check_http_status(r.status_code)

    def check_http_status(self, http_status):
        """ Checks if given HTTP status code is within the list at \
         ``TwitterSearch.exceptions`` and raises a ``TwitterSearchException`` \
         if this is the case. Example usage: ``checkHTTPStatus(200)`` and \
         ``checkHTTPStatus(401)``

        :param http_status: Integer value of the HTTP status of the \
        last query. Invalid statuses will raise an exception.
        :raises: TwitterSearchException
        """

        if http_status in self.exceptions:
            raise TwitterSearchException(http_status,
                                         self.exceptions[http_status])

    def search_tweets_iterable(self, order, callback=None):
        """ Returns itself and queries the Twitter API. Is called when using \
        an instance of this class as iterable. \
        See `Basic usage <basic_usage.html>`_ for examples

        :param order: An instance of TwitterOrder class \
        (e.g. TwitterSearchOrder or TwitterUserOrder)
        :param callback: Function to be called after a new page \
        is queried from the Twitter API
        :returns: Itself using ``self`` keyword
        """

        if callback:
            if not callable(callback):
                raise TwitterSearchException(1018)
            self.__callback = callback

        self.search_tweets(order)
        return self

    def get_minimal_id(self):
        """ Returns the minimal tweet ID of the current response

        :returns: minimal tweet identification number
        :raises: TwitterSearchException
        """

        if not self.__response:
            raise TwitterSearchException(1013)

        return min(
            self.__response['content']['statuses'] if self.__order_is_search
            else self.__response['content'],
            key=lambda i: i['id']
            )['id'] - 1

    def send_search(self, url):
        """ Queries the Twitter API with a given query string and \
        stores the results internally. Also validates returned HTTP status \
        code and throws an exception in case of invalid HTTP states. \
        Example usage ``sendSearch('?q=One+Two&count=100')``

        :param url: A string of the URL to send the query to
        :raises: TwitterSearchException
        """

        if not isinstance(url, str if py3k else basestring):
            raise TwitterSearchException(1009)

        endpoint = self._base_url + (self._search_url
                                     if self.__order_is_search
                                     else self._user_url)

        r = requests.get(endpoint + url,
                         auth=self.__oauth,
                         proxies={"https": self.__proxy})

        self.__response['meta'] = r.headers

        self.check_http_status(r.status_code)

        self.__response['content'] = r.json()

        # update statistics if everything worked fine so far
        seen_tweets = self.get_amount_of_tweets()
        self.__statistics[0] += 1
        self.__statistics[1] += seen_tweets

        # call callback if available
        if self.__callback:
            self.__callback(self)

        # if we've seen the correct amount of tweets there may be some more
        # using IDs to request more results
        # (former versions used page parameter)
        # see https://dev.twitter.com/docs/working-with-timelines

        # a leading ? char does "confuse" parse_qs()
        if url[0] == '?':
            url = url[1:]
        given_count = int(parse_qs(url)['count'][0])

        # Search API does have valid count values
        if self.__order_is_search and seen_tweets == given_count:
            self.__next_max_id = self.get_minimal_id()

        # Timelines doesn't have valid count values
        # see: https://dev.twitter.com/docs/faq
        # see section: "How do I properly navigate a timeline?"
        elif (not self.__order_is_search and
              len(self.__response['content']) > 0):
            self.__next_max_id = self.get_minimal_id()

        else:  # we got less tweets than requested -> no more results in API
            self.__next_max_id = None

        return self.__response['meta'], self.__response['content']

    def search_tweets(self, order):
        """ Creates an query string through a given TwitterSearchOrder \
        instance and takes care that it is send to the Twitter API. \
        This method queries the Twitter API **without** iterating or \
        reloading of further results and returns response. \
        See `Advanced usage <advanced_usage.html>`_ for example

        :param order: A TwitterOrder instance. \
        Can be either TwitterSearchOrder or TwitterUserOrder
        :returns: Unmodified response as ``dict``.
        :raises: TwitterSearchException
        """

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
        """ Triggers the search for more results using the Twitter API. \
        Raises exception if no further results can be found. \
        See `Advanced usage <advanced_usage.html>`_ for example

        :returns: ``True`` if there are more results available \
        within the Twitter Search API
        :raises: TwitterSearchException
        """

        if not self.__next_max_id:
            raise TwitterSearchException(1011)

        self.send_search(
            "%s&max_id=%i" % (self._start_url, self.__next_max_id)
        )
        return True

    def get_metadata(self):
        """ Returns all available meta data collected during last query. \
        See `Advanced usage <advanced_usage.html>`_ for example

        :returns: Available meta information about the \
        last query in form of a ``dict``
        :raises: TwitterSearchException
        """

        if not self.__response:
            raise TwitterSearchException(1012)
        return self.__response['meta']

    def get_tweets(self):
        """ Returns all available data from last query. \
        See `Advanced usage <advanced_usage.html>`_ for example

        :returns: All tweets found using the last query as a ``dict``
        :raises: TwitterSearchException
        """

        if not self.__response:
            raise TwitterSearchException(1013)
        return self.__response['content']

    def get_statistics(self):
        """ Returns dict with statistical information about \
        amount of queries and received tweets. Returns statistical values \
        about the number of queries and the sum of all tweets received by \
        this very instance of :class:`TwitterSearch`. \
        Example usage: ``print("Queries done: %i. Tweets received: %i"
        % ts.get_statistics())``

        :returns: A ``tuple`` with ``queries`` and \
        ``tweets`` keys containing integers. E.g. ``(1,100)`` which stands \
        for one query that contained one hundred tweets.
        """

        return (self.__statistics[0], self.__statistics[1])

    def get_amount_of_tweets(self):
        """ Returns current amount of tweets available within this instance

        :returns: The amount of tweets currently available
        :raises: TwitterSearchException
        """

        if not self.__response:
            raise TwitterSearchException(1013)

        return (len(self.__response['content']['statuses'])
                if self.__order_is_search
                else len(self.__response['content']))

    def set_supported_languages(self, order):
        """ Loads currently supported languages from Twitter API \
        and sets them in a given TwitterSearchOrder instance.
        See `Advanced usage <advanced_usage.html>`_ for example

        :param order: A TwitterOrder instance. \
        Can be either TwitterSearchOrder or TwitterUserOrder
        """

        if not isinstance(order, TwitterSearchOrder):
            raise TwitterSearchException(1010)

        r = requests.get(self._base_url + self._lang_url,
                         auth=self.__oauth,
                         proxies={"https": self.__proxy})

        self.__response['meta'] = r.headers
        self.check_http_status(r.status_code)
        self.__response['content'] = r.json()

        order.iso_6391 = []
        for lang in self.__response['content']:
            order.iso_6391.append(lang['code'])

    # Iteration
    def __iter__(self):
        self.__next_tweet = 0
        return self

    def next(self):
        """ Python2 comparability method. Simply returns ``self.__next__()``

        :returns: the ``__next__()`` method of this class
        """

        return self.__next__()

    def __next__(self):
        if not self.__response:
            raise TwitterSearchException(1014)

        if self.__next_tweet < self.get_amount_of_tweets():
            self.__next_tweet += 1
            if self.__order_is_search:
                return (self.__response['content']
                        ['statuses'][self.__next_tweet-1])
            else:
                return self.__response['content'][self.__next_tweet-1]

        try:
            self.search_next_results()
        except TwitterSearchException:
            raise StopIteration

        if self.get_amount_of_tweets() != 0:
            self.__next_tweet = 1
            if self.__order_is_search:
                return (self.__response['content']
                        ['statuses'][self.__next_tweet-1])
            else:
                return self.__response['content'][self.__next_tweet-1]
        raise StopIteration
