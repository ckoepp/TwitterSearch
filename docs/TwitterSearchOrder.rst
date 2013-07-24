TwitterSearchOrder
==================

This class mainly acts as a plain container for configuration all parameters currently available by the Twitter Search API.

If you're looking for the exceptions this class raises, please have a look at the article about `TwitterSearchException <TwitterSearchException.html>`_.


Available methods
-----------------

There are several parameters which can easily be set and modified by methods in *TwitterSearchOrder*. 

The only parameter with a default value is ``count`` with *100*. This is because it is the maximum of tweets returned by the Twitter API and in most cases you'd like to reduce traffic and the amount of queries, so it makes sense to set the biggest possible value by default.

Be aware that some parameters *can be* ignored by Twitter. For example currently not every language is detectable by the Search API. TwitterSearch is only responsible for transmitting values according to the Twitter documentation.

================ ============== ================================================================================ ==========================================================
API Parameter    Type           Modifying methods                                                                Example
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
q                ***required*** ``addKeyword(<string>)``, ``setKeywords(<list>)``                                ``addKeyword('#Hashtag')``, ``setKeywords(['foo','bar'])``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
geocode          *optional*     ``setGeocode(latitude<float>, longitude<float>, radius<int,long>, unit<mi,km>)`` ``setGeocode(52.5233,13.4127,10,'km')``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
lang             *optional*     ``setLanguage(<ISO-6391-string>)``                                               ``setLanguage('en')``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
locale           *optional*     ``setLocale(<ISO-6391-string>)``                                                 ``setLocale('ja')``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
result_type      *optional*     ``setResultType(<mixed,recent,popular>)``                                        ``setResultType('recent')``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
count            *optional*     ``setCount(<int>[Range: 1-100])``                                                ``setCount(42)``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
until            *optional*     ``setUntil(<datetime.date>)``                                                    ``setUntil(datetime.date(2012, 12, 24))``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
since_id         *optional*     ``setSinceID(<int,long>[Range: >0])``                                            ``setSinceID(250075927172759552)``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
max_id           *optional*     ``setMaxID(<int,long>[Range: >0])``                                              ``setMaxID(249292149810667520)``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
include_entities *optional*     ``setIncludeEntities(<bool,int>)``                                               ``setIncludeEntities(True)``, ``setIncludeEntities(1)``
---------------- -------------- -------------------------------------------------------------------------------- ----------------------------------------------------------
callback         *optional*     ``setCallback(<string>)``                                                        ``setCallback('myMethod')``
================ ============== ================================================================================ ==========================================================

If you're not familar with the meaning of the parameters, please have a look at the `Twitter Search API documentation <https://dev.twitter.com/docs/api/1.1/get/search/tweets>`_. Most parameter are self-descriping anyway.

Advanced usage
--------------

You may want to use *TwitterSearchOrder* for just generating a valid Twitter Search API query string containing all your arguments without knowing too much details about the Twitter API? No problem at all as there is the method ``TwitterSearchOrder.createSearchURL()``. It creates and returns an valid Twitter Search API query string. Afterwards the last created string is also available through ``TwitterSearchOrder.url``.

.. code-block:: python

	from TwitterSearch import TwitterSearchOrder, TwitterSearchException
	
	try:
	    tso = TwitterSearchOrder()
	    tso.setLanguage('nl')
	    tso.setLocale('ja')
	    tso.setKeywords(['One','Two'])
	    tso.addKeyword('myKeyword')
	
	    print(tso.createSearchURL())
	
	except TwitterSearchException as e:
    		print(e)

You'll receive ``?q=One+Two+myKeyword&count=100&lang=nl&locale=ja`` as result. Now you are free to use this string for manually querying Twitter (or any other API using the same parameter as Twitter does).

Maybe you would like to create another *TwitterSearchOrder* instance with a slightly other URL.

.. code-block:: python
	
	from TwitterSearch import TwitterSearchOrder, TwitterSearchException
	
	try:
	    tso = TwitterSearchOrder()
	    tso.setLanguage('nl')
	    tso.setLocale('ja')
	    tso.setKeywords(['One','Two'])
	    tso.addKeyword('myKeyword')
	
	    querystr = tso.createSearchURL()
	
	    # create a new TwitterSearchOrder based on the old query string and work with it
	    tso2 = TwitterSearchOrder()
	    tso2.setSearchURL(querystr + '&result_type=mixed&include_entities=true')
	    tso2.setLocale('en')
	    print(tso2.createSearchURL())
	
	except TwitterSearchException as e:
   	 print(e)

This piece of code will finally result in an output of ``?q=One+Two+myKeyword&count=100&lang=nl&locale=en&result_type=mixed&include_entities=true``.

Please be aware that the sense of arguments given by ``setSearchURL()`` is not checked. Due to this it is perfectly valid to to stuff like ``setSearchURL('q=Not+my+department&count=1731&locale=Canada&foo=bar')``. When manually setting the string, the leading ``?`` sign is optional.

Such stuff doesn't make much sense when querying Twitter. However, there may be cases when you're using TwitterSearch is some exotic context where this behavior is needed to avoid the regular checks of the *TwitterSearchOrder* methods.

Be aware that if you're using ``setSearchURL()`` all previous configured parameters are lost.
