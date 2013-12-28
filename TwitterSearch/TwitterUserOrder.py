# -*- coding: utf-8 -*-

import datetime
from .TwitterSearchException import TwitterSearchException
from .TwitterOrder import TwitterOrder
from .utils import py3k

try: from urllib.parse import parse_qs, quote_plus, unquote # python3
except ImportError: from urlparse import parse_qs; from urllib import quote_plus, unquote #python2

class TwitterUserOrder(TwitterOrder):
    """
    This class configures all arguments available of the user_timeline endpoint of the Twitter API (version 1.1 only).

    It also creates a valid query string out of the current configuration.
    """

    _max_count = 200

    def __init__(self, user):
        """ Argument user can be either a ID or screen-name of a user """
        self.arguments.update({ 'count' : '%s' % self._max_count })
        self.set_include_rts(True) # see: https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline
        self.set_exclude_replies(False)
        self.url = ''

        if py3k:
            if isinstance(user, int):
                self.arguments.update( { 'user_id' : '%i' % user } )
            elif isinstance(user, str):
                self.arguments.update( { 'screen_name' : user } )
            else:
                raise TwitterSearchException(1017)
        else:
            if isinstance(user, (int, long)):
                self.arguments.update( { 'user_id' : '%i' % user } )
            elif isinstance(user, basestring):
                self.arguments.update( { 'screen_name' : user } )
            else:
                raise TwitterSearchException(1017)

    def set_trim_user(self, trim):
        """ Sets 'trim_user' paramater """
        if not isinstance(trim, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if trim else 'false' } )

    def set_include_rts(self, rts):
        """ Sets 'include_rts' paramater """
        if not isinstance(rts, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if rts else 'false' } )

    def set_exclude_replies(self, exclude):
        """ Sets 'exclude_replies' paramater """
        if not isinstance(exclude, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if exclude else 'false' } )

    def set_contributor_details(self, contdetails):
        """ Sets 'contributor_details' paramater """
        if not isinstance(contdetails, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if contdetails else 'false' } )

    def create_search_url(self):
        """ Generates (urlencoded) query string from stored key-values tuples """
        url = '?'
        for key, value in self.arguments.items():
            url += '%s=%s&' % (quote_plus(key), quote_plus(value))
        self.url = url[:-1]
        return self.url

    def set_search_url(self, url):
        """ Reads given query string and stores key-value tuples """
        if url[0] == '?':
            url = url[1:]

        self.arguments = {}
        for key, value in parse_qs(url).items():
            self.arguments.update({key : unquote(value[0])})
