
Advanced usage: The :class:`TwitterUserOrder` class
=====================================================

This class mainly acts as a plain container for configuration all parameters currently available by the Twitter Search API. There are several parameters which can easily be set and modified by methods in :class:`TwitterSearchOrder`. 

The only parameter with a default value is ``count`` with *200*. This is because it is the maximum of tweets returned by this very Twitter API endpoint. In most cases you'd like to reduce traffic and the amount of queries, so it makes sense to set the biggest possible value by default. Please note that this endpoint has a different maximum size than the one used in :class:`TwitterSearchOrder`.


=================== ============== ================================================================================================= =============================================================
API Parameter       Type           Modifying methods                                                                                 Example
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
user_id             *optional*     constructor (either screen-name or ID of user required)                                           ``TwitterUserOrder("some_username")``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
screen_name         *optional*     constructor (either screen-name or ID of user required)                                           ``TwitterUserOrder(123457890)``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
count               *optional*     ``set_count(<int>[Range: 1-200])``                                                                ``set_count(42)``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
until               *optional*     ``set_until(<datetime.date>)``                                                                    ``set_until(datetime.date(2012, 12, 24))``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
since_id            *optional*     ``set_since_id(<int,long>[Range: >0])``                                                           ``set_since_id(250075927172759552)``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
max_id              *optional*     ``set_max_id(<int,long>[Range: >0])``                                                             ``set_max_id(249292149810667520)``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
trim_user           *optional*     ``set_trim_user(<bool>)``                                                                         ``set_trim_user(True)``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
exclude_replies     *optional*     ``set_exclude_replies(<bool>)``                                                                   ``set_exclude_replies(False)``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
contributor_details *optional*     ``set_contributor_details(<bool>)``                                                               ``set_contributor_details(True)``
------------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
include_rts         *optional*     ``set_include_rts(<bool>)``                                                                       ``set_include_rts(True)``
=================== ============== ================================================================================================= =============================================================

If you're not familiar with the meaning of the parameters, please have a look at the `Twitter User Timeline API documentation <https://dev.twitter.com/rest/reference/get/statuses/user_timeline>`_. Most parameter are self-describing anyway. Only special use-cases may require those detailed configuration values to be set, so don't worry if you don't touch one of those advanced methods in your code.


Advanced usage examples
-----------------------

You may want to use :class:`TwitterUserOrder` for just generating a valid Twitter Search API query string containing all your arguments without knowing too much details about the Twitter API? No problem at all as there is the method ``TwitterUserOrder.createSearchURL()``. It creates and returns an valid Twitter Search API query string. Afterwards the last created string is also available through ``TwitterSearchOrder.url``.

.. code-block:: python

  from TwitterSearch import TwitterUserOrder, TwitterSearchException
  
  try:
      tuo = TwitterUserOrder("some_user")
      tuo.set_trim_user(True)
      tuo.set_exclude_replies(False)
      tuo.set_include_rts(True)
  
      print(tuo.create_search_url())
  
  except TwitterSearchException as e:
        print(e)

You'll receive ``?trim_user=true&exclude_replies=false&include_rts=true`` as result. Now you are free to use this string for manually querying Twitter (or any other API using the same parameter as Twitter does).

Maybe you would like to create a new instance of :class:`TwitterUserOrder` with the same configuration but for a different user. This is one way to do exactly this:

.. code-block:: python
  
  from TwitterSearch import TwitterSearchOrder, TwitterSearchException
  
  try:
      tuo = TwitterUserOrder("some_user")
      tuo.set_trim_user(True)
      tuo.set_exclude_replies(False)
      tuo.set_include_rts(True)
  
      querystr = tuo.createSearchURL()
  
      # create a new TwitterSearchOrder based on the old query string and work with it
      tuo2 = TwitterUserOrder("some_other_user")
      tuo2.set_search_url(querystr)

      print(tso2.create_search_url())
  
  except TwitterSearchException as e:
     print(e)

This piece of code will also result in an output of ``?trim_user=true&exclude_replies=false&include_rts=true``.

Please be aware that the sense of arguments given by ``set_search_url()`` is not checked. Due to this it is perfectly valid to to stuff like ``set_search_url('?trim_user=true&exclude_replies=false&include_rts=true&count=1337&foo=bar')``. When manually setting the string, the leading ``?`` sign is optional. Due to this you can force TwitterSearch to request custom queries. But be aware that those non-compatible queries are likely to fail. Use such techniques with caution as it doesn't make much sense when querying Twitter. However, there may be cases when you're using TwitterSearch is some exotic context where this behavior is needed to avoid the regular checks of the :class:`TwitterUserOrder` methods. 

Also note that if you're using ``set_search_url()`` all previous configured parameters are lost and overridden.
