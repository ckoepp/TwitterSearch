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


class TwitterUserOrder(TwitterOrder):
    """
    This class configures all arguments available of the
    user_timeline endpoint of the Twitter API (version 1.1 only).
    It also creates a valid query string out of the current configuration.
    """

    _max_count = 200

    def __init__(self, user):
        """ Argument user can be either a ID or screen-name of a user

        :param user: Either string or integer/long value \
        of twitter user to query time-line from
        :raises: TwitterSearchException
        """

        self.arguments.update({'count': '%s' % self._max_count})

        # see: https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline
        self.set_include_rts(True)

        self.set_exclude_replies(False)
        self.url = ''

        if py3k:
            if isinstance(user, int):
                self.arguments.update({'user_id': '%i' % user})
            elif isinstance(user, str):
                self.arguments.update({'screen_name': user})
            else:
                raise TwitterSearchException(1017)
        else:
            if isinstance(user, (int, long)):
                self.arguments.update({'user_id': '%i' % user})
            elif isinstance(user, basestring):
                self.arguments.update({'screen_name': user})
            else:
                raise TwitterSearchException(1017)

    def set_trim_user(self, trim):
        """ Sets 'trim_user' parameter. When set to True, \
        each tweet returned in a timeline will include a \
        user object including only the status authors numerical ID

        :param trim: Boolean triggering the usage of the parameter
        :raises: TwitterSearchException
        """

        if not isinstance(trim, bool):
            raise TwitterSearchException(1008)
        self.arguments.update({'trim_user': 'true' if trim else 'false'})

    def set_include_rts(self, rts):
        """ Sets 'include_rts' parameter. When set to False, \
        the timeline will strip any native retweets from the returned timeline

        :param rts: Boolean triggering the usage of the parameter
        :raises: TwitterSearchException
        """

        if not isinstance(rts, bool):
            raise TwitterSearchException(1008)
        self.arguments.update({'include_rts': 'true' if rts else 'false'})

    def set_exclude_replies(self, exclude):
        """ Sets 'exclude_replies' parameter used to \
        prevent replies from appearing in the returned timeline

        :param exclude: Boolean triggering the usage of the parameter
        :raises: TwitterSearchException
        """

        if not isinstance(exclude, bool):
            raise TwitterSearchException(1008)
        self.arguments.update({'exclude_replies': 'true'
                                                  if exclude
                                                  else 'false'})

    def set_contributor_details(self, contdetails):
        """ Sets 'contributor_details' parameter used to enhance the \
        contributors element of the status response to include \
        the screen_name of the contributor. By default only \
        the user_id of the contributor is included

        :param contdetails: Boolean triggering the usage of the parameter
        :raises: TwitterSearchException
        """

        if not isinstance(contdetails, bool):
            raise TwitterSearchException(1008)
        self.arguments.update({'contributor_details': 'true'
                                                      if contdetails
                                                      else 'false'})

    def create_search_url(self):
        """ Generates (urlencoded) query string from stored key-values tuples

        :returns: A string containing all arguments in a url-encoded format
        """

        url = '?'
        for key, value in self.arguments.items():
            url += '%s=%s&' % (quote_plus(key), quote_plus(value))
        self.url = url[:-1]
        return self.url

    def set_search_url(self, url):
        """ Reads given query string and stores key-value tuples

        :param url: A string containing a valid URL to parse arguments from
        """

        if url[0] == '?':
            url = url[1:]

        self.arguments = {}
        for key, value in parse_qs(url).items():
            self.arguments.update({key: unquote(value[0])})
