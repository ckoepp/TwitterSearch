# -*- coding: utf-8 -*-


class TwitterSearchException(Exception):
    """
    This class is all about exceptions (surprise, surprise!).
    All exception based directly on TwitterSearch will consist of
    a **code** and a **message** describing the reason of the
    exception shortly.
    """

    # HTTP status codes are stored in TwitterSearch.exceptions due
    # to possible on-the-fly modifications
    _error_codes = {
        1000: 'Neither a list nor a string',
        1001: 'Not a list object',
        1002: 'No ISO 6391-1 language code',
        1003: 'No valid result type',
        1004: 'Invalid number',
        1005: 'Invalid unit',
        1006: 'Invalid callback string',
        1007: 'Not a date object',
        1008: 'Invalid boolean',
        1009: 'Invalid string',
        1010: 'Not a valid TwitterSearchOrder object',
        1011: 'No more results available',
        1012: 'No meta data available',
        1013: 'No tweets available',
        1014: 'No results available',
        1015: 'No keywords given',
        1016: 'Invalid dict',
        1017: 'Invalid argument: need either a user ID or a screen-name',
        1018: 'Not a callable function',
    }

    def __init__(self, code, msg=None):
        self.code = code
        if msg:
            self.message = msg
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)
