
Advanced usage: The :class:`TwitterSearchOrder` class
=====================================================

This class mainly acts as a plain container for configuration all parameters currently available by the Twitter Search API. There are several parameters which can easily be set and modified by methods in :class:`TwitterSearchOrder`. 

The only parameter with a default value is ``count`` with *100*. This is because it is the maximum of tweets returned by this very Twitter API endpoint. In most cases you'd like to reduce traffic and the amount of queries, so it makes sense to set the biggest possible value by default. Please note that this endpoint has a different maximum size than the one used in :class:`TwitterUserOrder`.

Be aware that some parameters *can be* ignored by Twitter. For example currently not every language is detectable by the Search API. TwitterSearch is only responsible for transmitting values according to the Twitter documentation.

================ ============== ================================================================================================= =============================================================
API Parameter    Type           Modifying methods                                                                   Example
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
q                ***required*** ``add_keyword(<string>)``, ``set_keywords(<list>)``                                               ``add_keyword('#Hashtag')``, ``set_keywords(['foo','bar'])``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
geocode          *optional*     ``set_geocode(latitude<float>, longitude<float>, radius<int,long>, imperial_metric=<True,False>`` ``set_geocode(52.5233,13.4127,10,imperial_metric=True)``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
lang             *optional*     ``set_language(<ISO-6391-string>)``                                                               ``set_language('en')``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
locale           *optional*     ``set_locale(<ISO-6391-string>)``                                                                 ``set_locale('ja')``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
result_type      *optional*     ``set_result_type(<mixed,recent,popular>)``                                                       ``set_result_type('recent')``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
count            *optional*     ``set_count(<int>[Range: 1-100])``                                                                ``set_count(42)``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
until            *optional*     ``set_until(<datetime.date>)``                                                                    ``set_until(datetime.date(2012, 12, 24))``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
since_id         *optional*     ``set_since_id(<int,long>[Range: >0])``                                                           ``set_since_id(250075927172759552)``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
max_id           *optional*     ``set_max_id(<int,long>[Range: >0])``                                                             ``set_max_id(249292149810667520)``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
include_entities *optional*     ``set_include_etities(<bool,int>)``                                                               ``set_include_etities(True)``, ``set_include_etities(1)``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
callback         *optional*     ``set_callback(<string>)``                                                                        ``set_callback('myMethod')``
================ ============== ================================================================================================= =============================================================

If you're not familiar with the meaning of the parameters, please have a look at the `Twitter Search API documentation <https://dev.twitter.com/docs/api/1.1/get/search/tweets>`_. Most parameter are self-describing anyway. 


Advanced usage examples
-----------------------

You may want to use :class:`TwitterSearchOrder` for just generating a valid Twitter Search API query string containing all your arguments without knowing too much details about the Twitter API? No problem at all as there is the method ``TwitterSearchOrder.createSearchURL()``. It creates and returns an valid Twitter Search API query string. Afterwards the last created string is also available through ``TwitterSearchOrder.url``.

.. code-block:: python

  from TwitterSearch import TwitterSearchOrder, TwitterSearchException
  
  try:
      tso = TwitterSearchOrder()
      tso.set_language('nl')
      tso.set_locale('ja')
      tso.set_keywords(['One','Two'])
      tso.add_keyword('myKeyword')
  
      print(tso.create_search_url())
  
  except TwitterSearchException as e:
        print(e)

You'll receive ``?q=One+Two+myKeyword&count=100&lang=nl&locale=ja`` as result. Now you are free to use this string for manually querying Twitter (or any other API using the same parameter as Twitter does).

Maybe you would like to create another :class:`TwitterSearchOrder` instance with a slightly different URL.

.. code-block:: python
  
  from TwitterSearch import TwitterSearchOrder, TwitterSearchException
  
  try:
      tso = TwitterSearchOrder()
      tso.set_language('nl')
      tso.set_locale('ja')
      tso.set_keywords(['One','Two'])
      tso.add_keyword('myKeyword')
  
      querystr = tso.create_search_url()
  
      # create a new TwitterSearchOrder based on the old query string and work with it
      tso2 = TwitterSearchOrder()
      tso2.set_search_url(querystr + '&result_type=mixed&include_entities=true')
      tso2.set_locale('en')
      print(tso2.create_search_url())
  
  except TwitterSearchException as e:
     print(e)

This piece of code will finally result in an output of ``?q=One+Two+myKeyword&count=100&lang=nl&locale=en&result_type=mixed&include_entities=true``.

Please be aware that the sense of arguments given by ``set_search_url()`` is not checked. Due to this it is perfectly valid to to stuff like ``set_search_url('q=Not+my+department&count=1731&locale=Canada&foo=bar')``. When manually setting the string, the leading ``?`` sign is optional.

Such stuff doesn't make much sense when querying Twitter. However, there may be cases when you're using TwitterSearch is some exotic context where this behavior is needed to avoid the regular checks of the :class:`TwitterSearchOrder` methods. 

Be aware that if you're using ``set_search_url()`` all previous configured parameters are lost.

