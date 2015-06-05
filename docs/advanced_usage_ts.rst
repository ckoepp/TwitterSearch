Advanced usage: The :class:`TwitterSearch` class
================================================

This is the main class of this library where all the action takes place. There are many ways to use it and the most common ones are explained in this section.


Constructor of :class:`TwitterSearch`
-------------------------------------

The constructor needed to set your credentials for the Twitter API. The parameters are ``__init__( consumer_key, consumer_secret, access_token, access_token_secret, verify=True)``.

If you're new to Python take a look at the following example:

.. code-block:: python

    ts1 = TwitterSearch(
        consumer_key = 'aaabbb',
        consumer_secret = 'cccddd',
        access_token = '111222',
        access_token_secret = '333444'
    )

    # equals

    ts2 = TwitterSearch('aaabbb', 'cccddd', '111222', '333444', verify=True, proxy=None)


Authentication and verification
-------------------------------

Please be aware that there is **no further check** whether or not your credentials are valid if you set ``verify=False`` in the constructor. If you're skipping the verification process of :class:`TwitterSearch` you can avoid some traffic and one query. Note that this validation query is part of the rate-limiting as done by Twitter. If you are sure your credentials are correct you can disable this feature.

But be aware that you're only saving **one** request at all by avoiding the automatic verification process. Due to the fact that json doesn't consume much traffic at all, this may only be a way for very conservative developers or some exotic scenarios.

Proxy usage
-----------

To use a HTTPS proxy at initialization of the :class:`TwitterSearch` class, an addition argument named ``proxy='some.proxy:888'`` can be used. Otherwise the authentication will fail if the client has no direct access to the Twitter API.

Avoid rate-limitation using a callback method
----------------------------------------------

Sometimes there is the need to build in certain delays in order to avoid being `rate-limited <https://dev.twitter.com/rest/public/rate-limiting>`_ by Twitter. One way to add an artificial delay to your queries is to use the build-in module ``time`` of Python in combination with a callback method. The following example demonstrates how to use the ``callback`` argument of the ``TwitterSearch.search_tweets_iterable()`` method properly. In this particular case every 5th call to the Twitter API activates a delay of 60 seconds.

.. code-block:: python

    from TwitterSearch import *
    import time

    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['foo', 'bar'])
        
        ts = TwitterSearch(
            consumer_key = 'aaabbb',
            consumer_secret = 'cccddd',
            access_token = '111222',
            access_token_secret = '333444'
         )
        
        def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
            queries, tweets_seen = current_ts_instance.get_statistics()
            if queries > 0 and (queries % 5) == 0: # trigger delay every 5th query
                time.sleep(60) # sleep for 60 seconds

        for tweet in ts.search_tweets_iterable(tso, callback=my_callback_closure):
            print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
        
    except TwitterSearchException as e:
        print(e)

Remember that the callback is called every time a query to the Twitter API is performed. It's in your responsibility to make sure that your code doesn't have any unwanted side-effects or throws unintended exceptions. Also, every closure submitted via the ``callback`` argument is called with a the current instance of :class:`TwitterSearch`. Performing a delay is just one way to use this callback pattern.


Avoid rate-limitation manually
------------------------------

As you might know there is a certain amount of `meta-data <#access-meta-data>`_ available when using *TwitterSearch*. Some users might want to rely only on the ``get_statistics()`` method of the :class:`TwitterSearch` to trigger, for example, an artificial delay. This function returns a tuple of two integers. The first integer represents the amount of queries sent to Twitter so far, while the second one is an automatically increasing counter of the so far received tweets during those queries. Thus, an example taking those two meta-information into account could look like:

.. code-block:: python

    from TwitterSearch import *
    import time

    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['foo', 'bar'])
        
        ts = TwitterSearch(
            consumer_key = 'aaabbb',
            consumer_secret = 'cccddd',
            access_token = '111222',
            access_token_secret = '333444'
         )
        
        sleep_for = 60 # sleep for 60 seconds
        last_amount_of_queries = 0 # used to detect when new queries are done

        for tweet in ts.search_tweets_iterable(tso):
            print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

            current_amount_of_queries = ts.get_statistics()[0]
            if not last_amount_of_queries == current_amount_of_queries:
                last_amount_of_queries = current_amount_of_queries
                time.sleep(sleep_for)
        
    except TwitterSearchException as e:
        print(e)


Returned tweets
---------------

This library is trying to not hide anything from your eyes except the complexity of its functions. Due to this you're able to get all the information available (which can be quite a lot).

Example output with only one tweet included:

.. code-block:: python

    {'search_metadata': {'completed_in': 0.08,
                     'count': 1,
                     'max_id': 352072665667878913,
                     'max_id_str': '352072665667878913',
                     'next_results': '?max_id=352072665667878912&q=Germany%20castle&count=1&include_entities=1',
                     'query': 'Germany+castle',
                     'refresh_url': '?since_id=352072665667878913&q=Germany%20castle&include_entities=1',
                     'since_id': 0,
                     'since_id_str': '0'},
                     'statuses': [
                     {'contributors': None,
               'coordinates': None,
               'created_at': 'Tue Jul 02 14:33:59 +0000 2013',
               'entities': {'hashtags': [],
                            'media': [{'display_url': 'pic.twitter.com/Oz77FLEong',
                                       'expanded_url': 'http://twitter.com/ThatsEarth/status/351839174887870464/photo/1',
                                       'id': 351839174896259072,
                                       'id_str': '351839174896259072',
                                       'indices': [117, 139],
                                       'media_url': 'http://pbs.twimg.com/media/BOH73Y3CEAAldKU.jpg',
                                       'media_url_https': 'https://pbs.twimg.com/media/BOH73Y3CEAAldKU.jpg',
                                       'sizes': {'large': {'h': 639,
                                                           'resize': 'fit',
                                                           'w': 960},
                                                 'medium': {'h': 399,
                                                            'resize': 'fit',
                                                            'w': 600},
                                                 'small': {'h': 226,
                                                           'resize': 'fit',
                                                           'w': 340},
                                                 'thumb': {'h': 150,
                                                           'resize': 'crop',
                                                           'w': 150}},
                                       'source_status_id': 351839174887870464,
                                       'source_status_id_str': '351839174887870464',
                                       'type': 'photo',
                                       'url': 'http://t.co/Oz77FLEong'}],
                            'symbols': [],
                            'urls': [],
                            'user_mentions': [{'id': 118504288,
                                               'id_str': '118504288',
                                               'indices': [0, 11],
                                               'name': 'Josh Dallas',
                                               'screen_name': 'joshdallas'},
                                              {'id': 298250825,
                                               'id_str': '298250825',
                                               'indices': [12, 25],
                                               'name': 'Ginnifer Goodwin',
                                               'screen_name': 'ginnygoodwin'},
                                              {'id': 1201661238,
                                               'id_str': '1201661238',
                                               'indices': [49, 60],
                                               'name': 'Earth Pics',
                                               'screen_name': 'ThatsEarth'}]},
               'favorite_count': 0,
               'favorited': False,
               'geo': None,
               'id': 352072665667878913,
               'id_str': '352072665667878913',
               'in_reply_to_screen_name': 'joshdallas',
               'in_reply_to_status_id': None,
               'in_reply_to_status_id_str': None,
               'in_reply_to_user_id': 118504288,
               'in_reply_to_user_id_str': '118504288',
               'lang': 'en',
               'metadata': {'iso_language_code': 'en',
                            'result_type': 'recent'},
               'place': None,
               'possibly_sensitive': False,
               'retweet_count': 0,
               'retweeted': False,
               'source': '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>',
               'text': '@joshdallas @ginnygoodwin home during wintertime"@ThatsEarth: Hohenzollern Castle floating above the Clouds,Germany. http://t.co/Oz77FLEong"',
               'truncated': False,
               'user': {'contributors_enabled': False,
                        'created_at': 'Fri Aug 14 09:15:27 +0000 2009',
                        'default_profile': False,
                        'default_profile_image': False,
                        'description': 'Scorpio. 23. MBA Graduate.',
                        'entities': {'description': {'urls': []},
                                     'url': {'urls': [{'display_url': 'fanfiction.net/u/4764512/',
                                                       'expanded_url': 'http://www.fanfiction.net/u/4764512/',
                                                       'indices': [0,
                                                                   22],
                                                       'url': 'http://t.co/sEKQ1M85H2'}]}},
                        'favourites_count': 114,
                        'follow_request_sent': False,
                        'followers_count': 300,
                        'following': False,
                        'friends_count': 229,
                        'geo_enabled': False,
                        'id': 65599486,
                        'id_str': '65599486',
                        'is_translator': False,
                        'lang': 'en',
                        'listed_count': 0,
                        'location': 'Kuwait',
                        'name': 'Amal Behbehani',
                        'notifications': False,
                        'profile_background_color': 'DBE9ED',
                        'profile_background_image_url': 'http://a0.twimg.com/profile_background_images/317569734/tumblr_lqc4ttwuJm1qclkveo1_500.jpg',
                        'profile_background_image_url_https': 'https://si0.twimg.com/profile_background_images/317569734/tumblr_lqc4ttwuJm1qclkveo1_500.jpg',
                        'profile_background_tile': True,
                        'profile_banner_url': 'https://pbs.twimg.com/profile_banners/65599486/1372576102',
                        'profile_image_url': 'http://a0.twimg.com/profile_images/3763288269/57c274f19592f6d190957d8eb86c64f1_normal.png',
                        'profile_image_url_https': 'https://si0.twimg.com/profile_images/3763288269/57c274f19592f6d190957d8eb86c64f1_normal.png',
                        'profile_link_color': 'CC3366',
                        'profile_sidebar_border_color': 'DBE9ED',
                        'profile_sidebar_fill_color': 'E6F6F9',
                        'profile_text_color': '333333',
                        'profile_use_background_image': True,
                        'protected': False,
                        'screen_name': 'TigeyGirl',
                        'statuses_count': 18891,
                        'time_zone': 'Santiago',
                        'url': 'http://t.co/sEKQ1M85H2',
                        'utc_offset': -14400,
                        'verified': False}}]}

Have a look at the `entities documented by Twitter <https://dev.twitter.com/docs/platform-objects/entities>`_ to figure out what a specific key-value tuple does exactly mean.

Access meta data
----------------

An output of the available meta data from the query to the Twitter API is stored in a ``dict`` structure. You can access it by calling ``get_metadata()`` which will return all meta information about the last query.

Example:

.. code-block:: python

    { 
    'content-length': '467129', 
    'x-rate-limit-reset': '1372773784', 
    'x-rate-limit-remaining': '170', 
    'x-xss-protection': '1; mode=block', 
    'cache-control': 'no-cache, no-store, must-revalidate, pre-check=0, post-check=0', 
    'status': '200', 
    'transfer-encoding': 'chunked', 
    'set-cookie': 'lang=de, guest_id=v1%!xxx; Domain=.twitter.com; Path=/; Expires=Thu, 01-Jul-2013 14:02:32 UTC',
    'expires': 'Tue, 31 Mar 1981 05:00:00 GMT',
    'x-access-level': 'read',
    'last-modified': 'Tue, 01 Jul 2013 14:02:32 GMT', 
    '-content-encoding': 'gzip', 
    'pragma': 'no-cache', 
    'date': 'Tue, 01 Jul 2013 14:02:32 GMT',
    'x-rate-limit-limit': '180',
    'content-location': u'https://api.twitter.com/1.1/search/tweets.json?count=100&oauth_body_hash=xxx&oauth_nonce=xxx&oauth_timestamp=xxx&oauth_consumer_key=xxx&oauth_signature_method=HMAC-SHA1&q=Germany+castle&oauth_version=1.0&oauth_token=xxx&oauth_signature=xxx', 
    'x-transaction': 'xxx', 
    'strict-transport-security': 'max-age=631138519',
    'server': 'tfe',
    'x-frame-options': 'SAMEORIGIN',
    'content-type': 'application/json;charset=utf-8'
    }

Be **careful** about those data as it contains sensible data as you can see in ``get_metadata()['content-location']``. Do **NOT** save or output those information to insecure environments!

If you are interested in the amount of queries that this library did automatically on your behalf you can access those information easily by calling ``get_statistcs()``. A trivial example use-case could be to print out those informations as part of a debugging or logging facility: ``print("Queries done: %i. Tweets received: %i" % ts.get_statistics())``


TwitterSearch without automatic iteration
-----------------------------------------

It is also perfectly possible to use *TwitterSearch* without any automatic iteration and to query the Twitter API all by yourself. For example you may like to implement the `suggest max_id procedure of Twitter <https://dev.twitter.com/docs/working-with-timelines>`_ to access the API directly and don't trust the library to do this automatically on its own. Just assume that we would like to implement this feature independently again. A possible solution of this could look like:

.. code-block:: python

    from TwitterSearch import *

    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['Germany', 'castle'])

        ts = TwitterSearch('aaabbb', 'cccddd', '111222', '333444')

        # init variables needed in loop
        todo = True
        next_max_id = 0

        # let's start the action
        while(todo):

            # first query the Twitter API
            response = ts.search_tweets(tso)

            # print rate limiting status
            print( "Current rate-limiting status: %i" % ts.get_metadata()['x-rate-limit-reset'])

            # check if there are statuses returned and whether we still have work to do
            todo = not len(response['content']['statuses']) == 0

            # check all tweets according to their ID
            for tweet in response['content']['statuses']:
                tweet_id = tweet['id']
                print("Seen tweet with ID %i" % tweet_id)

                # current ID is lower than current next_max_id?
                if (tweet_id < next_max_id) or (next_max_id == 0):
                    next_max_id = tweet_id
                    next_max_id -= 1 # decrement to avoid seeing this tweet again

            # set lowest ID as MaxID
            tso.set_max_id(next_max_id)

    except TwitterSearchException as e:
        print(e)


On-the-fly loading of supported languages
-----------------------------------------

As you may have figured out some languages are not supported by Twitter and those that are may change over time. This is why Twitter does provide `an endpoint <https://dev.twitter.com/docs/api/1.1/get/help/languages>`_ to load all currently supported languages. You may query it to gather current information about the languages in Twitter.


.. code-block:: python

        from TwitterSearch import *

        try:
            tso = TwitterSearchOrder()
            ts = TwitterSearch('aaabbb', 'cccddd', '111222', '333444')

            # load  currently supported languages by Twitter and store them in a TwitterSearchOrder object
            ts.set_supported_languages(tso)

            # try to set German (see ISO 639-1) as language 
            ts.set_language('de')
            print('German seems to be officially supported by Twitter. Yay!')

        except TwitterSearchException as e:
        
            # if we get an 1002 code it means that 'de' is not supported (see TwitterSearchException)
            if e.code == 1002:
                print('Oh no - German is not supported :(')
            print(e)
