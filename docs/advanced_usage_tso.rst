
Advanced usage: The :class:`TwitterSearchOrder` class
=====================================================

This class mainly acts as a plain container for configuration all parameters currently available by the Twitter Search API. There are several parameters which can easily be set and modified by methods in :class:`TwitterSearchOrder`. 

The only parameter with a default value is ``count`` with *100*. This is because it is the maximum of tweets returned by this very Twitter API endpoint. In most cases you'd like to reduce traffic and the amount of queries, so it makes sense to set the biggest possible value by default. Please note that this endpoint has a different maximum size than the one used in :class:`TwitterUserOrder`.

Be aware that some parameters *can be* ignored by Twitter. For example currently not every language is detectable by the Search API. TwitterSearch is only responsible for transmitting values according to the Twitter documentation.

================ ============== ================================================================================================= =============================================================
API Parameter    Type           Modifying methods                                                                                 Example
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
q                ***required*** ``add_keyword(<string>)``, ``add_keyword(<list>, or_operator=True)``, ``set_keywords(<list>)``    ``add_keyword('#Hashtag')``, ``set_keywords(['foo','bar'])``

---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
q                *optional*     ``set_link_filter()``, ``remove_link_filter()``                                                   ``set_link_filter()``, ``remove_link_filter()``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
q                *optional*     ``set_question_filter()``, ``remove_question_filter)``                                            ``set_question_filter()``, ``remove_question_filter)`` 
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
q                *optional*     ``set_source_filter(<string>)``, ``remove_source_filter)``                                        ``set_source_filter('twitterfeed')``
---------------- -------------- ------------------------------------------------------------------------------------------------- -------------------------------------------------------------
q                *optional*     ``set_positive_attitude_filter()``, ``set_negative_attitude_filter``, ``remove_attitude_filter)`` ``set_positive_attitude_filter()``
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


Advanced filtering
------------------

There are certain types of filters the Twitter Search API can handle. All of them are listed in the `Twitter documentation <https://dev.twitter.com/rest/public/search>`_. Unfortunately such advanced filters can be quite messy. Read this chapter if you'd like to use advanced queries of the Twitter API. All filters **not** based on keyword can be removed by using ``TwitterSearchOrder.remove_all_filters()``.

Keywords with spaces
~~~~~~~~~~~~~~~~~~~~

Twitter does search for keywords separately by default. This means looking for ``James Bond`` will return tweets containing the words ``James`` and ``Bond`` like in ``There was a bond of friendship between James and Amy``. However, sometimes you might like to look for reviews of the newest ``James Bond`` movie and therefore such tweets won't be much of a help for you. In this case make sure to add a keyword surrounded by ``"``. Twitter will take such keywords as one phrase resulting in tweets actually containing ``James Bond`` like in ``My name is Bond ... James Bond``.

*TwitterSearch* will handle those issues for you by default as calling ``add_keyword("James Bond")`` will look for ``"James Bond"`` as one full phrase while ``add_keyword(["James","Bond"])`` will result in a search for `James AND Bond`.

Excepting keywords
~~~~~~~~~~~~~~~~~~

Sometimes you might like to look for tweets containing specific words but not containing a different one. It's easy to except a certain keyword by applying a dash prefix (``-``) to it. Thus, a line like ``set_keywords(['Porsche', '-Fiat'])`` will give you all tweets containing the word ``Porsche`` but only if there is no ``Fiat`` in it.

OR concatenating of keywords
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to search for ``foo OR bar`` with *TwitterSearch*. Instead of simply adding those keywords like we did in the basic usage chapter, you can use the ``or_operator=True`` parameter. It's also possible to concatenate different keyword:

.. code-block:: python

    from TwitterSearch import *
    
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['Goofy', 'Nyancat'], or_operator = True)
        tso.add_keyword('BMW')
        
        ts = TwitterSearch(
                consumer_key = 'aaabbb',
                consumer_secret = 'cccddd',
                access_token = '111222',
                access_token_secret = '333444'
            )
        
        for tweet in ts.search_tweets_iterable(tso):
            print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
    
        except TwitterSearchException as e:
            print(e)

Concatenating several keywords can be tricky as the syntax of the Twitter Search API is pretty undocumented and only roughly defined. In my tests it turned out at a query like ``Goofy OR Nycancat BMW`` seemed to be the very same as ``(Goofy OR Nycancat) AND BMW`` although there is nothing mentioned in the documentation about concatenations of keywords. If you'd like to make sure your combination works, better use the `official Twitter Search <https://twitter.com/search-home>`_ to perform some tests and see whether Twitter handles your query correctly.


Tweets of/from/mentioning a certain user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example we'll use the twitter account of Eric Jarosinski and his twitter user `Nein Quarterly <https://twitter.com/neinquarterly>`_.

It's also possible to search for tweets of a certain user. You'd better use :class:`TwitterUserOrder` for this as this actually queries the timeline of the user instead of using the Twitter Search API. Nonetheless, it's also possible to do through :class:`TwitterSearchOrder`. Just add the prefix of ``from:`` to the username. Using standard *TwitterSearch* methods this would look like ``add_keyword("from:neinquarterly")``.

Tweets directly to a user can be collected using the ``to:`` prefix in front of the username. Due to this tweets to ``neinquarterly`` can be collected using ``add_keyword("to:neinquarterly")``.

If you'd like to receive tweets referencing a certain user you are able to gather them by using a ``@`` prefix in front of the username.  Thus, the corresponding code snipped is ``add_keyword("@neinquarterly")``.

Tweets with hyperlinks
~~~~~~~~~~~~~~~~~~~~~~

In a different scenario you might be only interested in tweets containing a hyperlink. You can look for those tweets using the filter method of *TwitterSearch*:

.. code-block:: python

    from TwitterSearch import *
    
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['Mickey', '#Mouse'], or_operator = True)
        tso.set_link_filter()
        
        ts = TwitterSearch(
                consumer_key = 'aaabbb',
                consumer_secret = 'cccddd',
                access_token = '111222',
                access_token_secret = '333444'
            )
        
        for tweet in ts.search_tweets_iterable(tso):
            print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
    
        except TwitterSearchException as e:
            print(e)


This will return all tweets with a hyperlink in them and containing the keyword ``Mickey`` or the hashtag ``#Mouse``. To remove a already set link filter, the method ``remove_link_filter()`` was added.

Tweets containing a question
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's also possible to receive only tweets that are asking a question. You can do so by setting the filter via ``TwitterSearchOrder.set_question_filter()``. A removal of this filter can be done with ``TwitterSearchOrder.remove_question_filter()``. Be aware that this filtering is done by Twitter and it doesn't necessary work well as it might miss questions in certain languages.

Attitude filtering
~~~~~~~~~~~~~~~~~~

Twitter also offers an attitude-based filtering mechanism. You can search for positive tweets by using ``TwitterSearchOrder.set_positive_attitude_filter()`` and for negative ones by using ``TwitterSearchOrder.set_negative_attitude_filter()``. The attitude filtering can be removed using ``TwitterSearchOrder.remove_attitude_filter()``. Note that this filter mechanism is performed by Twitter directly and you may miss tweets not detected by those. This especially holds true for tweets not authored in English.

Source filtering
~~~~~~~~~~~~~~~~

If you're interested in tweets only submitted using a specific software you can do so using the method ``TwitterSearchOrder.set_source_filter(<string>)``. Calling ``set_source_filter("twitterfeed")`` gives you only tweets submitted using `TwitterFeed <http://twitterfeed.com/>`_. The removal of this filter can be performed through ``TwitterSearchOrder.remove_source_filter()``.

Time-based filtering
~~~~~~~~~~~~~~~~~~~~

*TwitterSearch* tries to concentrate on simple query and does prefer to submit arguments as parameters instead of merging them into the query string. Thus *TwitterSearch* will generate raw query strings like ``?q=foobar&until=2010-12-27`` instead of ``?q=foobar+since:2010-12-27``. Both versions will return the very same tweets but while the first one separates the values in different parameters, the second one just merges everything together. Doing so is likely to lead to long and possibly wrong query strings. Remember that you're perfectly able to submit stuff like ``?q=foobar+since:2010-12-27+until:2010-12-26`` which is obviously non-sense. If you would still like to dump everything into the ``q`` parameter you can do so manually by using ``set_keywords(['since:2010-12-27','until:2010-12-26'])`` for example.

If you have no specific reason to actually include those time-based filters into the search query parameter directly, you should use the default methods of ``set_since_id()`` and/or ``set_until()``.

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
