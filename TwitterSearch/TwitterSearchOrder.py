# -*- coding: utf-8 -*-

import datetime
from .TwitterSearchException import TwitterSearchException
from .TwitterOrder import TwitterOrder
from .utils import py3k

try:
    from urllib.parse import parse_qs, quote_plus, unquote  # python3
except ImportError:
    from urlparse import parse_qs
    from urllib import quote_plus, unquote  # python2


class TwitterSearchOrder(TwitterOrder):
    """
    This class is for configurating all available
    arguments of the Twitter Search API (v1.1). It also creates valid query
    strings which can be used in other environments identical to the
    syntax of the Twitter Search API.
    """

    # default value for count should be the maximum value to minimize traffic
    # see https://dev.twitter.com/docs/api/1.1/get/search/tweets
    _max_count = 100

    # taken from http://www.loc.gov/standards/iso639-2/php/English_list.php
    iso_6391 = ['aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as',
                'av', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bm',
                'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr',
                'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'ee',
                'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi',
                'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu',
                'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy',
                'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is',
                'it', 'iu', 'ja', 'jv', 'ka', 'kg', 'ki', 'kj', 'kk',
                'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'kv', 'kw', 'ky',
                'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv',
                'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt',
                'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no',
                'nr', 'nv', 'ny', 'oc', 'oj', 'om', 'or', 'os', 'pa',
                'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru',
                'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl',
                'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv',
                'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn',
                'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur',
                'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo',
                'za', 'zh', 'zu']

    def __init__(self):
        """ Constructor """

        self.arguments = {'count': '%s' % self._max_count}
        self.searchterms = []
        self.url = ''

    def add_keyword(self, word):
        """ Adds a given string or list to the current keyword list

        :param word: String or list of at least 2 character long keyword(s)
        :raises: TwitterSearchException
        """

        if isinstance(word, str if py3k else basestring) and len(word) >= 2:
            self.searchterms.append(word)
        elif isinstance(word, list):
            self.searchterms += word
        else:
            raise TwitterSearchException(1000)

    def set_keywords(self, words):
        """ Sets a given list as the new keyword list

        :param words: A list of at least 2 character long new keywords
        :raises: TwitterSearchException
        """

        if not isinstance(words, list):
            raise TwitterSearchException(1001)
        self.searchterms = words

    def set_search_url(self, url):
        """ Reads given query string and stores key-value tuples

        :param url: A string containing a valid URL to parse arguments from
        """

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
            self.arguments.update({key: unquote(value[0])})

    def create_search_url(self):
        """ Generates (urlencoded) query string from stored key-values tuples

        :returns: A string containing all arguments in a url-encoded format
        """

        if len(self.searchterms) == 0:
            raise TwitterSearchException(1015)

        url = '?q='
        url += '+'.join([quote_plus(i) for i in self.searchterms])

        for key, value in self.arguments.items():
            url += '&%s=%s' % (quote_plus(key), (quote_plus(value)
                                                 if key != 'geocode'
                                                 else value))

        self.url = url
        return self.url

    def set_language(self, lang):
        """ Sets 'lang' parameter used to only fetch tweets within \
        a certain language

        :param lang: A 2-letter language code string (ISO 6391 compatible)
        :raises: TwitterSearchException
        """

        if lang in self.iso_6391:
            self.arguments.update({'lang': '%s' % lang})
        else:
            raise TwitterSearchException(1002)

    def set_locale(self, lang):
        """ Sets 'locale' parameter to specify the language \
        of the query you are sending (only ja is currently effective)

        :param lang: A 2-letter language code string (ISO 6391 compatible)
        :raises: TwitterSearchException
        """

        if lang in self.iso_6391:
            self.arguments.update({'locale': '%s' % lang})
        else:
            raise TwitterSearchException(1002)

    def set_result_type(self, result_type):
        """ Sets 'result_type' parameter to specify what type of search \
        results you would prefer to receive. The current default is “mixed.” \
        Valid values include: \
            - mixed: Include both popular and real time results \
            - recent: return only the most recent results \
            - popular: return only the most popular results \

        :param result_type: A string containing one of \
        the three valid result types

        :raises: TwitterSearchException
        """

        result_type = result_type.lower()
        if result_type in ['mixed', 'recent', 'popular']:
            self.arguments.update({'result_type': '%s' % result_type})
        else:
            raise TwitterSearchException(1003)

    def set_geocode(self, latitude, longitude, radius, imperial_metric=True):
        """ Sets geolocation parameters to return only tweets by users \
        located within a given radius of the given latitude/longitude. \
        The location is preferentially taking from the Geotagging API, \
        but will fall back to their Twitter profile.

        :param latitude: A integer or long describing the latitude
        :param longitude: A integer or long describing the longitude
        :param radius: A integer or long describing the radius
        :param imperial_metric: Whether the radius is given in metric \
        (kilometers) or imperial (miles) system. \
        Default is ``True`` which relates to usage of the \
        imperial kilometer metric
        :raises: TwitterSearchException

        """

        if not isinstance(radius, int if py3k else (int, long)) or radius <= 0:
            raise TwitterSearchException(1004)

        if isinstance(latitude, float) and isinstance(longitude, float):
            if isinstance(imperial_metric, bool):
                self.arguments.update({'geocode': '%s,%s,%s%s' % (latitude,
                                                                  longitude,
                                                                  radius,
                                                                  'km'
                                                                  if imperial_metric
                                                                  else 'mi')})
            else:
                raise TwitterSearchException(1005)
        else:
            raise TwitterSearchException(1004)

    def set_callback(self, func):
        """ Sets 'callback' parameter. If supplied, the response \
        will use the JSONP format with a callback of the given name

        :param func: A string containing the name of the callback function
        :raises: TwitterSearchException
        """

        if isinstance(func, str if py3k else basestring) and func:
            self.arguments.update({'callback': '%s' % func})
        else:
            raise TwitterSearchException(1006)

    def set_until(self, date):
        """ Sets 'until' parameter used to return \
        only tweets generated before the given date

        :param date: A datetime instance
        :raises: TwitterSearchException
        """

        if isinstance(date, datetime.date) and date <= datetime.date.today():
            self.arguments.update({'until': '%s' % date.strftime('%Y-%m-%d')})
        else:
            raise TwitterSearchException(1007)
