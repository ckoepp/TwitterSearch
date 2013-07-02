import simplejson
import oauth2 as oauth
from sys import maxint
from urlparse import parse_qs
from TwitterSearchException import TwitterSearchException
from TwitterSearchOrder import TwitterSearchOrder

class TwitterSearch(object):
    base_url = 'https://api.twitter.com/1.1/'
    verify_url = 'account/verify_credentials.json'
    search_url = 'search/tweets.json'

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

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, authenticate=True):
        # app
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

        # user
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret

        # init internal variables
        self._response = {}
        self._nextMaxID = maxint

        # statistics
        self._statistics = { 'queries' : 0, 'tweets' : 0 }

        # verify
        if authenticate:
            self.authenticate(True)

    def isNextpage(self):
        if nextpage:
            return True
        return False

    def authenticate(self, verify=False):
        consumer = oauth.Consumer(key = self.__consumer_key, secret = self.__consumer_secret)
        token = oauth.Token(key = self.__access_token, secret = self.__access_token_secret)
        self.__client = oauth.Client(consumer, token)

        if verify:
            meta, response = self.__client.request(self.base_url + self.verify_url, 'GET')
            self.checkHTTPStatus(int(meta['status']))

    def checkHTTPStatus(self, http_status):
        if http_status in self.exceptions:
            raise TwitterSearchException(http_status, self.exceptions[http_status])

    def searchTweetsIterable(self, order):
        self.searchTweets(order)
        return self

    def sentSearch(self, url):
        if not isinstance(url, basestring):
            raise TwitterSearchException(1009)
        self._response['meta'], content = self.__client.request(self.base_url + self.search_url + url, 'GET')

        self.checkHTTPStatus(int(self._response['meta']['status']))

        # using IDs to request more results - former versions used page parameter
        # see https://dev.twitter.com/docs/working-with-timelines
        given_count = parse_qs(url)['count'][0]
        self._response['content'] = simplejson.loads(content)

        self._statistics['queries'] += 1
        self._statistics['tweets'] += len(self._response['content']['statuses'])

        if self._response['content']['search_metadata']['count'] < given_count:
            # have a look for the lowest ID
            for tweet in self._response['content']['statuses']:
              if tweet['id'] < self._nextMaxID:
                  self._nextMaxID = tweet['id']
            self._nextMaxID -= 1
        else:
            self._nextMaxID = None

        return self._response['meta'], self._response['content']

    def searchTweets(self, order):
        if not isinstance(order, TwitterSearchOrder):
            raise TwitterSearchException(1010)

        self._startURL = order.createSearchURL()
        self.sentSearch(self._startURL)
        return self._response

    def searchNextResults(self):
        if not self._nextMaxID:
            raise TwitterSearchException(1011)

        self.sentSearch("%s&max_id=%i" % (self._startURL, self._nextMaxID))
        return self._response

    def getMetadata(self):
        if not self._response:
            raise TwitterSearchException(1012)
        return self._response['meta']

    def getTweets(self):
        if not self._response:
           raise TwitterSearchException(1013)
        return self._response['content']

    def getStatistics(self):
        return self._statistics

    # Iteration
    def __iter__(self):
        if not self._response:
            raise TwitterSearchException(1014)
        self._nextTweet = 0
        return self

    def next(self):
        if self._nextTweet < len(self._response['content']['statuses']):
            self._nextTweet += 1
            return self._response['content']['statuses'][self._nextTweet-1]

        try:
            self.searchNextResults()
        except TwitterSearchException:
            raise StopIteration

        if len(self._response['content']['statuses']) != 0:
            self._nextTweet = 1
            return self._response['content']['statuses'][self._nextTweet-1]
        raise StopIteration
