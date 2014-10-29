# -*- coding: utf-8 -*-

from .TwitterSearchException import TwitterSearchException
from .utils import py3k


class TwitterOrder(object):
    """ Basic interface class to inherit from.
    Methods raising NotImplementedError exceptions need to be
    implemented by all children
    """

    arguments = {}

    def create_search_url(self):
        """ Generates an url-encoded query string from \
        stored key-values tuples. Has to be implemented \
        within child classes

        :raises: NotImplementedError
        """

        raise NotImplementedError

    def set_search_url(self, url):
        """ Reads given query string and stores key-value tuples. \
        Has to be implemented within child classes

        :param url: A string containing the twitter API endpoint URL
        :raises: NotImplementedError
        """

        raise NotImplementedError

    def set_since_id(self, twid):
        """ Sets 'since_id' parameter used to return only results \
        with an ID greater than (that is, more recent than) the specified ID

        :param twid: A valid tweet ID in either long (Py2k) \
        or integer (Py2k + Py3k) format
        :raises: TwitterSearchException
        """

        if py3k:
            if not isinstance(twid, int):
                raise TwitterSearchException(1004)
        else:
            if not isinstance(twid, (int, long)):
                raise TwitterSearchException(1004)

        if twid > 0:
            self.arguments.update({'since_id': '%s' % twid})
        else:
            raise TwitterSearchException(1004)

    def set_max_id(self, twid):
        """ Sets 'max_id' parameter used to return only results \
        with an ID less than (that is, older than) or equal to the specified ID

        :param twid: A valid tweet ID in either long (Py2k) \
        or integer (Py2k + Py3k) format
        :raises: TwitterSearchException
        """

        if py3k:
            if not isinstance(twid, int):
                raise TwitterSearchException(1004)
        else:
            if not isinstance(twid, (int, long)):
                raise TwitterSearchException(1004)

        if twid > 0:
            self.arguments.update({'max_id': '%s' % twid})
        else:
            raise TwitterSearchException(1004)

    def set_count(self, cnt):
        """ Sets 'count' parameter used to define the number of \
        tweets to return per page. Maximum and default value is 100

        :param cnt: Integer containing the number of tweets per \
        page within a range of 1 to 100
        :raises: TwitterSearchException
        """

        if isinstance(cnt, int) and cnt > 0 and cnt <= 100:
            self.arguments.update({'count': '%s' % cnt})
        else:
            raise TwitterSearchException(1004)

    def set_include_entities(self, include):
        """ Sets 'include entities' parameter to either \
        include or exclude the entities node within the results

        :param include: Boolean to trigger the 'include entities' parameter
        :raises: TwitterSearchException
        """

        if not isinstance(include, bool):
            raise TwitterSearchException(1008)
        self.arguments.update(
            {'include_entities': 'true' if include else 'false'}
        )
