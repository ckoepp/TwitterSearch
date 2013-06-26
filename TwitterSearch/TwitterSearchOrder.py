import urllib
import datetime
from TwitterSearchException import TwitterSearchException

class TwitterSearchOrder(object):

    # taken from http://www.loc.gov/standards/iso639-2/php/English_list.php
    iso_6391 = ['aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as', 'av', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bm', 'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr', 'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'ee', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi', 'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'ka', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'kv', 'kw', 'ky', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny', 'oc', 'oj', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']

    def __init__(self):
        self.arguments = {}
        self.searchterms = []
        self.url = ''
        self.manual_url = False

    def addKeyword(self, word):
        if isinstance(word, basestring) and word:
            self.searchterms.append(word)
        elif isinstance(word, list):
            self.searchterms += word
        else:
            raise TwitterSearchException(1000)

    def setKeywords(self, word):
        if not isinstance(word, list):
            raise TwitterSearchException(1001)
        self.searchterms = word

    def setSearchURL(self, url):
        self.manual_url = True
        self.url = url
        return self.url

    def createSearchURL(self):
        if self.manual_url:
            return self.url

        url = '?'
        url += 'q='
        for term in self.searchterms:
            url += '%s+' % urllib.quote_plus(term)
        url = url[0:len(url)-1]

        for key, value in self.arguments.iteritems():
            url += '&' +'%s=%s' % (urllib.quote_plus(key), urllib.quote_plus(value))

        self.url = url
        return self.url

    def setLanguage(self, lang):
        if len(lang) == 2 and lang in self.iso_6391:
            self.arguments.update( { 'lang' : '%s' % lang } )
        else:
            raise TwitterSearchException(1002)

    def setLocale(self, lang):
        if len(lang) == 2 and lang in self.iso_6391:
            self.arguments.update( { 'locale' : '%s' % lang } )
        else:
            raise TwitterSearchException(1002)

    def setResultType(self, tor):
        if tor == 'mixed' or tor == 'recent' or tor == 'popular':
            self.arguments.update( { 'result_type' : '%s' % tor } )
        else:
            raise TwitterSearchException(1003)

    def setSinceID(self, twid):
        if isinstance(twid, (int, long)) and twid > 0:
            self.arguments.update( { 'since_id' : '%s' % twid } )
        else:
            raise TwitterSearchException(1004)

    def setMaxID(self, twid):
        if isinstance(twid, (int, long)) and twid > 0:
            self.arguments.update( { 'max_id' : '%s' % twid } )
        else:
            raise TwitterSearchException(1004)

    def setCount(self, cnt):
        if isinstance(cnt, (int, long)) and cnt > 0:
            self.arguments.update( { 'count' : '%s' % cnt } )
        else:
            raise TwitterSearchException(1004)

    def setGeocode(self, latitude, longitude, radius, unit):
        if isinstance(latitude, float) and isinstance(longitude, float) and isinstance(radius, (long, int)):
            if unit == 'mi' or unit == 'km':
                self.arguments.update( { 'geocode' : '%s,%s,%s%s' % (latitude, longitude, radius, unit) } )
            else:
                raise TwitterSearchException(1005)
        else:
            raise TwitterSearchException(1004)

    def setCallback(self, func):
        if isinstance(func, basestring) and func:
            self.arguments.update( { 'callback' : '%s' % func } )
        else:
            raise TwitterSearchException(1006)

    def setUntil(self, date):
        if isinstance(date, datetime.date):
            self.arguments.update( { 'unitl' : '%s' % date.strftime('%Y-%m-%d') } ) 
        else:
            raise TwitterSearchException(1007)

    def setIncludeEntities(self, include):
        if not isinstance(include, (bool, int)) and ( include == 1 or include == 0):
            raise TwitterSearchException(1008)

        if include:
            self.arguments.update( { 'include_entities' : 'True' } )
        else:
            self.arguments.update( { 'include_entities' : 'False' } )
