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
            elif isinstance(user, basestr):
                self.arguments.update( { 'screen_name' : user } )
            else:
                raise TwitterSearchException(1017)
                
    def setTrimUser(self, trim):
        """ Sets 'trim_user' paramater """
        if not isinstance(trim, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if trim else 'false' } )
        
    def setIncludeRts(self, rts):
        """ Sets 'include_rts' paramater """
        if not isinstance(rts, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if rts else 'false' } )
        
    def setExcludeReplies(self, exclude):
        """ Sets 'exclude_replies' paramater """
        if not isinstance(exclude, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if exclude else 'false' } )
        
    def setContributorDetails(self, contdetails):
        """ Sets 'contributor_details' paramater """
        if not isinstance(contdetails, bool):
            raise TwitterSearchException(1008)
        self.arguments.update( { 'trim_user' : 'true' if contdetails else 'false' } )
        
    def createSearchURL(self):
        """ Generates (urlencoded) query string from stored key-values tuples """
        url = '?'
        for key, value in self.arguments.items():
            url += '%s=%s&' % (quote_plus(key), quote_plus(value))
        self.url = url[:-1]
        return self.url

    def setSearchURL(self, url):
        """ Reads given query string and stores key-value tuples """
        if url[0] == '?':
            url = url[1:]

        self.arguments = {}
        for key, value in parse_qs(url).items():
            self.arguments.update({key : unquote(value[0])})
