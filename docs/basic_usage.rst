Basic usage
===========

In most cases you probably just like to iterate through all available tweets as easy as possible. And there it is, a very minimal example to do exactly this:

.. code-block:: python

    from TwitterSearch import *
    
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['#Hashtag1', '#Hashtag2'])
        
        ts = TwitterSearch(
                consumer_key = 'aaabbb',
                consumer_secret = 'cccddd',
                access_token = '111222',
                access_token_secret = '333444'
            )
        
        for tweet in ts.search_tweets_iterable(tso):
            print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
    
        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)

If you're into the access of a timeline of a certain user, you can do this by using the same pattern:

.. code-block:: python

  from TwitterSearch import *

  try:
      # create a TwitterUserOrder for user named 'NeinQuarterly'
      tuo = TwitterUserOrder('NeinQuarterly') # is equal to TwitterUserOrder(458966079)

      # it's about time to create TwitterSearch object again
      ts = TwitterSearch(
          consumer_key = 'aaabbb',
          consumer_secret = 'cccddd',
          access_token = '111222',
          access_token_secret = '333444'
      )

      # start asking Twitter about the timeline
      for tweet in ts.search_tweets_iterable(tuo):
          print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

  except TwitterSearchException as e: # catch all those ugly errors
      print(e)


Please note those code snippets are already working examples executable in both, Python2 **and** Python3.


Accessible information
----------------------

.. note::
    The Twitter Search API does not reveal tweets older than a week (or sometimes dating back to 10 days). Be aware that the official `Twitter Search <https://twitter.com/search-home>`_ does not use the Twitter Search API but a internal Twitter interface. Thus, it reveals tweets older than those you can collect through the public API. If you need access to old tweets you might have pay a commercial provider to give you access to its Twitter archives.

The creator of this library doesn't like to hide any informations from you. Therefore the data you'll receive is quite a lot. A typical tweet, as mentioned in the section above, consists of a huge ``dict``.

You may ask the question "*But what does this field exactly mean?*". Well, that's where the job of *TwitterSearch* ends and the `Twitter documentation <https://dev.twitter.com/docs/platform-objects/tweets>`_ joins the fun.

An example of how such a tweet looks like is the following dict:

.. code-block:: python

	{'contributors': None,
 'coordinates': None,
 'created_at': 'Tue Jul 02 11:43:18 +0000 2013',
 'entities': {'hashtags': [],
              'media': [{'display_url': 'pic.twitter.com/dJLxVZaSW9',
                         'expanded_url': 'http://twitter.com/EarthBeauties/status/351897277473882113/photo/1',
                         'id': 351897277478076417,
                         'id_str': '351897277478076417',
                         'indices': [78, 100],
                         'media_url': 'http://pbs.twimg.com/media/BOIwtZ2CAAEFRXU.jpg',
                         'media_url_https': 'https://pbs.twimg.com/media/BOIwtZ2CAAEFRXU.jpg',
                         'sizes': {'large': {'h': 375,
                                             'resize': 'fit',
                                             'w': 600},
                                   'medium': {'h': 375,
                                              'resize': 'fit',
                                              'w': 600},
                                   'small': {'h': 213,
                                             'resize': 'fit',
                                             'w': 340},
                                   'thumb': {'h': 150,
                                             'resize': 'crop',
                                             'w': 150}},
                         'source_status_id': 351897277473882113,
                         'source_status_id_str': '351897277473882113',
                         'type': 'photo',
                         'url': 'http://t.co/dJLxVZaSW9'}],
              'symbols': [],
              'urls': [],
              'user_mentions': [{'id': 786796010,
                                 'id_str': '786796010',
                                 'indices': [33, 47],
                                 'name': u'Earth Pictures\u2122',
                                 'screen_name': 'EarthBeauties'}]},
 'favorite_count': 0,
 'favorited': False,
 'geo': None,
 'id': 352029711347617792,
 'id_str': '352029711347617792',
 'in_reply_to_screen_name': 'EarthBeauties',
 'in_reply_to_status_id': 351897277473882113,
 'in_reply_to_status_id_str': '351897277473882113',
 'in_reply_to_user_id': 786796010,
 'in_reply_to_user_id_str': '786796010',
 'lang': 'in',
 'metadata': {'iso_language_code': 'in', 'result_type': 'recent'},
 'place': None,
 'possibly_sensitive': False,
 'retweet_count': 0,
 'retweeted': False,
 'source': 'web',
 'text': 'mau dong dibangunin rmh kekgini "@EarthBeauties: Hohenzollern Castle, Germany http://t.co/dJLxVZaSW9',
 'truncated': False,
 'user': {'contributors_enabled': False,
          'created_at': 'Sun Mar 18 04:22:51 +0000 2012',
          'default_profile': False,
          'default_profile_image': False,
          'description': u"girl non-smoking alcohol-free \u2022 @PLAYMAKERKIDSHC \u2022 DSFF \u2022 15\u221e \u2022 NotWild''",
          'entities': {'description': {'urls': []},
                       'url': {'urls': [{'display_url': 'instagram.com/giwaang',
                                         'expanded_url': 'http://instagram.com/giwaang',
                                         'indices': [0, 22],
                                         'url': 'http://t.co/vCyfkrdTwa'}]}},
          'favourites_count': 1,
          'follow_request_sent': False,
          'followers_count': 661,
          'following': False,
          'friends_count': 176,
          'geo_enabled': False,
          'id': 528140042,
          'id_str': '528140042',
          'is_translator': False,
          'lang': 'id',
          'listed_count': 1,
          'location': u"SwiekeCity\u2022PinkBabyRoom's",
          'name': 'EarStud',
          'notifications': False,
          'profile_background_color': 'BADFCD',
          'profile_background_image_url': 'http://a0.twimg.com/profile_background_images/872889954/b7439a65d39bdff360c934bd6f33c3b7.jpeg',
          'profile_background_image_url_https': 'https://si0.twimg.com/profile_background_images/872889954/b7439a65d39bdff360c934bd6f33c3b7.jpeg',
          'profile_background_tile': True,
          'profile_banner_url': 'https://pbs.twimg.com/profile_banners/528140042/1369624796',
          'profile_image_url': 'http://a0.twimg.com/profile_images/378800000047155611/7581e79882f1c9f1bbe4b706a023e2c9_normal.jpeg',
          'profile_image_url_https': 'https://si0.twimg.com/profile_images/378800000047155611/7581e79882f1c9f1bbe4b706a023e2c9_normal.jpeg',
          'profile_link_color': 'FF0000',
          'profile_sidebar_border_color': '000000',
          'profile_sidebar_fill_color': '252429',
          'profile_text_color': '666666',
          'profile_use_background_image': True,
          'protected': False,
          'screen_name': 'giwaang',
          'statuses_count': 10199,
          'time_zone': None,
          'url': 'http://t.co/vCyfkrdTwa',
          'utc_offset': None,
          'verified': False}}

Architecture
------------

TwitterSearch consists of four classes: `TwitterSearch <TwitterSearch.html#module-TwitterSearch.TwitterSearch>`_, `TwitterSearchOrder <TwitterSearch.html#module-TwitterSearch.TwitterSearchOrder>`_, `TwitterUserOrder <TwitterSearch.html#module-TwitterSearch.TwitterUserOrder>`_ and `TwitterSearchException <TwitterSearch.html#module-TwitterSearch.TwitterSearchException>`_.

To not repeat certain code-fragments the class  `TwitterOrder <TwitterSearch.html#module-TwitterSearch.TwitterOrder>`_ is also available. However, this class is rarely used directly and only contains few basic methods.
