import urllib
from TwitterSearchException import TwitterSearchException

class TwitterSearchOrder(object):

    # taken from http://www.loc.gov/standards/iso639-2/php/English_list.php
    iso_6391 = ['aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as', 'av', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bm', 'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr', 'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'ee', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi', 'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'ka', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'kv', 'kw', 'ky', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny', 'oc', 'oj', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']

    def __init__(self):
        self.arguments = {}
        self.searchterms = []
        self.url = ''

    def addKeyword(self, word):
        if isinstance(word, basestring):
            self.searchterms.append(word)
        elif isinstance(word, list):
            self.searchterms = self.searchterms + word
        else:
            raise TwitterSearchException('Neither a list nor a string')

    def setKeywords(self, word):
        if not isinstance(word, list):
            raise TwitterSearchException('Not a list object')
        self.searchterms = word

    def setSearchURL(self, url):
        self.url = url
        return self.url

    def createSearchURL(self):
        url = '?'

        url += 'q='
        for term in self.searchterms:
            url += '%s+' % urllib.quote_plus(term)
        url = url[0:len(url)-1]

        for key, value in self.arguments.iteritems():
            url += '&' +'%s=%s' % (urllib.quote_plus(key), urllib.quote_plus(value))

        return self.setSearchURL(url)

    def setLanguage(self, lang):
        if len(lang) == 2 and lang in self.iso_6391:
            self.arguments.update( { 'lang' : '%s' % lang } )
        else:
            raise TwitterSearchException('No ISO 6391-1 language code')

    def setCount(self, cnt):
        if isinstance(cnt, (int, long)):
            self.arguments.update( { 'count' : '%s' % cnt } )
        else:
            raise TwitterSearchException('Not a valid number')

    def setIncludeEntities(self, include):
        if not isinstance(include, (bool, int)) and ( include == 1 or include == 0):
            raise TwitterSearchException('Not a valid boolean')

        if include:
            self.arguments.update( { 'include_entities' : 'True' } )
        else:
            self.arguments.update( { 'include_entities' : 'False' } )
