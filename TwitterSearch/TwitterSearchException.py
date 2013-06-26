class TwitterSearchException(Exception):

   # HTTP status codes are stored in TwitterSearch.exceptions
    _error_codes = { 
        1000 : 'Neither a list nor a string',
        1001 : 'Not a list object',
        1002 : 'No ISO 6391-1 language code',
        1003 : 'No valid result type',
        1004 : 'Invalid number',
        1005 : 'Invalid unit',
        1006 : 'Invalid callback string',
        1007 : 'Not a date object',
        1008 : 'Invalid boolean',                
    }

    def __init__(self, code, msg = None):
        self.code = code
        if msg:
            self.message = msg
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %s: %s" % (self.code, self.message)
