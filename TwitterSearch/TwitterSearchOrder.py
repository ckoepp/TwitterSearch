import datetime
from .TwitterSearchException import TwitterSearchException
from .utils import py3k

try: from urllib.parse import parse_qs, quote_plus, unquote # python3
except ImportError: from urlparse import parse_qs; from urllib import quote_plus, unquote #python2

class TwitterSearchOrder(object):
    """
    This class is for configurating all available arguments of the Twitter Search API (v1.1).

    It also creates valid query strings which can be used in other environments identical to the syntax of the Twitter Search API.
    """

    # default value for count should be the maximum value to minimize traffic
    # see https://dev.twitter.com/docs/api/1.1/get/search/tweets
    _max_count = 100

    # taken from http://www.loc.gov/standards/iso639-2/php/English_list.php
    iso_6391 = ['aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as', 'av', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bm', 'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr', 'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'ee', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi', 'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'ka', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'kv', 'kw', 'ky', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny', 'oc', 'oj', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']

    def __init__(self):
        self.arguments = { 'count' : '%s' % self._max_count }
        self.searchterms = []
        self.url = ''

    def addKeyword(self, word):
        """ Adds a given string or list to the current keyword list """
        if isinstance(word, str if py3k else basestring) and len(word) >= 2:
          self.searchterms.append(word)
        elif isinstance(word, list):
            self.searchterms += word
        else:
            raise TwitterSearchException(1000)

    def setKeywords(self, word):
        """ Sets a given list as the new keyword list """
        if not isinstance(word, list):
            raise TwitterSearchException(1001)
        self.searchterms = word

    def setSearchURL(self, url):
        """ Reads given query string and stores key-value tuples """
        if url[0] == '?':
            url = url[1:]

        args = parse_qs(url)
        self.searchterms = args['q']
        del args['q']

        # urldecode keywords
        for item in self.searchterms:
            item = unquote(item)

        self.arguments = {}
        for key, value in args.items():
            self.arguments.update({key : unquote(value[0])})

    def createSearchURL(self):
        """ Generates (urlencoded) query string from stored key-values tuples """
        if len(self.searchterms) == 0:
            raise TwitterSearchException(1015)

        url = '?q='
        url += '+'.join([ quote_plus(i) for i in self.searchterms])

        for key, value in self.arguments.items():
            url += '&%s=%s' % (quote_plus(key), (quote_plus(value) if key != 'geocode' else value) )

        self.url = url
        return self.url

    def setLanguage(self, lang):
        """ Sets 'lang' paramater """
        if lang in self.iso_6391:
            self.arguments.update( { 'lang' : '%s' % lang } )
        else:
            raise TwitterSearchException(1002)

    def setLocale(self, lang):
        """ Sets 'locale' paramater """
        if lang in self.iso_6391:
            self.arguments.update( { 'locale' : '%s' % lang } )
        else:
            raise TwitterSearchException(1002)

    def setResultType(self, tor):
        """ Sets 'result_type' paramater """
        if tor == 'mixed' or tor == 'recent' or tor == 'popular':
            self.arguments.update( { 'result_type' : '%s' % tor } )
        else:
            raise TwitterSearchException(1003)

    def setSinceID(self, twid):
        """ Sets 'since_id' parameter """
        if py3k:
            if not isinstance(twid, int):
                raise TwitterSearchException(1004)
        else:
           if not isinstance(twid, (int, long)):
                raise TwitterSearchException(1004)

        if twid > 0:
            self.arguments.update( { 'since_id' : '%s' % twid } )
        else:
            raise TwitterSearchException(1004)

    def setMaxID(self, twid):
        """ Sets 'max_id' parameter """
        if py3k:
            if not isinstance(twid, int):
                raise TwitterSearchException(1004)
        else:
           if not isinstance(twid, (int, long)):
                raise TwitterSearchException(1004)

        if twid > 0:
            self.arguments.update( { 'max_id' : '%s' % twid } )
        else:
            raise TwitterSearchException(1004)

    def setCount(self, cnt):
        """ Sets 'count' paramater """
        if isinstance(cnt, int) and cnt > 0 and cnt <= 100:
            self.arguments.update( { 'count' : '%s' % cnt } )
        else:
            raise TwitterSearchException(1004)

    def setGeocode(self, latitude, longitude, radius, km=True):
        """ Sets geolocation paramaters """
        if not isinstance(radius, (int) if py3k else (int, long) ) or radius <= 0:
           raise TwitterSearchException(1004)

        if isinstance(latitude, float) and isinstance(longitude, float):
            if isinstance(km, bool):
                self.arguments.update( { 'geocode' : '%s,%s,%s%s' % (latitude, longitude, radius, 'km' if km else 'mi') } )
            else:
                raise TwitterSearchException(1005)
        else:
            raise TwitterSearchException(1004)

    def setCallback(self, func):
        """ Sets 'callback' paramater """
        if isinstance(func, str if py3k else basestring) and func:
            self.arguments.update( { 'callback' : '%s' % func } )
        else:
            raise TwitterSearchException(1006)

    def setUntil(self, date):
        """ Sets 'until' parameter """
        if isinstance(date, datetime.date) and date <= datetime.date.today():
            self.arguments.update( { 'until' : '%s' % date.strftime('%Y-%m-%d') } )
        else:
            raise TwitterSearchException(1007)

    def setIncludeEntities(self, include):
        """ Sets 'include entities' paramater """
        if not isinstance(include, bool):
            raise TwitterSearchException(1008)

        if include:
            self.arguments.update( { 'include_entities' : 'True' } )
        else:
            self.arguments.update( { 'include_entities' : 'False' } )
