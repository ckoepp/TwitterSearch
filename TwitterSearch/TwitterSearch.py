import simplejson
import oauth2 as oauth
from TwitterSearchException import TwitterSearchException
from TwitterSearchOrder import TwitterSearchOrder

class TwitterSearch(object):
    search_url = 'https://api.twitter.com/1.1/search/tweets.json'
    request_token_url = 'http://twitter.com/oauth/request_token'
    response = {}
    nextresults = None

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # app
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        # user
        self.access_token = access_token
        self.access_token_secret = access_token_secret

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
        self.nextTweet += 1
        if self.nextTweet < len(self.response['content']['statuses']):
            return self.response['content']['statuses'][self.nextTweet]

        try:
            self.searchNextResults()
        except TwitterSearchException:
            raise StopIteration
        if len(self.response['content']['statuses']) != 0:
            self.nextTweet = 0
            return self.response['content']['statuses'][self.nextTweet]
        raise StopIteration
