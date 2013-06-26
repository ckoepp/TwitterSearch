import simplejson
import oauth2 as oauth
from TwitterSearchException import TwitterSearchException
from TwitterSearchOrder import TwitterSearchOrder

class TwitterSearch(object):
    search_url = 'https://api.twitter.com/1.1/search/tweets.json'
    request_token_url = 'https://api.twitter.com/oauth/request_token'

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

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # app
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        # user
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        # init internal variables
        self.response = {}
        self.nextresults = None

    def isNextpage(self):
        if nextpage:
            return True
        return False

    def authenticate(self):
        consumer = oauth.Consumer(key = self.consumer_key, secret = self.consumer_secret)
        token = oauth.Token(key = self.access_token, secret = self.access_token_secret)
        self.client = oauth.Client(consumer, token)

    def searchTweetsIterable(self, order):
        self.searchTweets(order)
        return self

    def sentSearch(self, url):
        if not isinstance(url, basestring):
            raise TwitterSearchException('No valid string')
        self.response['meta'], content = self.client.request(self.search_url + url, 'GET')

        # raise exceptions based on http status
        http_status = int(self.response['meta']['status'])
        if http_status in self.exceptions:
            raise TwitterSearchException('HTTP status %i - %s' % (http_status, self.exceptions[http_status]))

        self.response['content'] = simplejson.loads(content)
        if self.response['content']['search_metadata'].get('next_results'):
            self.nextresults = self.response['content']['search_metadata']['next_results']
        else:
            self.nextresults = None
        return self.response['meta'], self.response['content']

    def searchTweets(self, order):
        if not isinstance(order, TwitterSearchOrder):
            raise TwitterSearchException('Not a valid TwitterSearchOrder object')

        self.sentSearch(order.createSearchURL())
        return self.response

    def searchNextResults(self):
        if not self.nextresults:
            raise TwitterSearchException('No more results available')

        self.sentSearch(self.nextresults)
        return self.response

    def getMetadata(self):
        if not self.response:
            raise TwitterSearchException('No meta available')
        return self.response['meta']

    def getTweets(self):
        if not self.response:
           raise TwitterSearchException('No tweets available')
        return self.response['content']

    def __iter__(self):
        if not self.response:
            raise TwitterSearchException('No results available')
        self.nextTweet = 0
        return self

    def next(self):
        if self.nextTweet < len(self.response['content']['statuses']):
            next = self.nextTweet
            self.nextTweet += 1
            return self.response['content']['statuses'][next]

        try:
            self.searchNextResults()
        except TwitterSearchException:
            raise StopIteration

        if len(self.response['content']['statuses']) != 0:
            self.nextTweet = 0
            return self.response['content']['statuses'][self.nextTweet]
        raise StopIteration
