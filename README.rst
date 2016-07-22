*************
TwitterSearch
*************

.. image:: https://img.shields.io/travis/ckoepp/TwitterSearch/master.svg?style=flat-square
    :target: http://travis-ci.org/ckoepp/TwitterSearch/branches
    :alt: Build Status

.. image:: https://img.shields.io/coveralls/ckoepp/TwitterSearch.svg?style=flat-square
    :target: https://coveralls.io/r/ckoepp/TwitterSearch?branch=master
    :alt: Coverage
    
.. image:: https://landscape.io/github/ckoepp/TwitterSearch/master/landscape.svg?style=flat-square
    :target: https://landscape.io/github/ckoepp/TwitterSearch/master
    :alt: Code Health

.. image:: https://img.shields.io/pypi/v/TwitterSearch.svg?style=flat-square
    :target: https://pypi.python.org/pypi/TwitterSearch/
    :alt: PyPi version
	
.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://raw.githubusercontent.com/ckoepp/TwitterSearch/master/LICENSE
    :alt: MIT License

.. image:: https://readthedocs.org/projects/twittersearch/badge/?version=latest
     :target: https://twittersearch.readthedocs.org/en/latest/
     :alt: Documentation

This library allows you easily create a search through the Twitter  API without having to know too much about the API details. Based on such a search you can even iterate throughout all tweets reachable via the Twitter Search API. There is an automatic reload of the next pages while using the iteration. TwitterSearch was developed as part of an interdisciplinary project at the `Technische Universität München <http://www.tum.de/en/>`_.

Reasons to use TwitterSearch
############################

Well, because it can be quite annoying to always parse the search url together and a minor spelling mistake is sometimes hard to find. Not to mention the pain of getting the next page of the results. Why not centralize this process and concentrate on the more important parts of the project?

More than that, TwitterSearch is:

* pretty small (around 500 lines of code currently)
* pretty easy to use, even for beginners
* pretty good at giving you **all** available information (including meta information)
* pretty iterable without any need to manually reload more results from the API
* pretty wrong values of API arguments are to raise an exception. This is done before the API gets queried and therefore helps to avoid to reach Twitters' limitations by obviously wrong API calls
* pretty friendly to Python >= 2.7 **and** Python >= 3.2
* pretty pretty to look at :)

Installation
############

TwitterSearch is also available on pypi and therefore can be installed via ``pip install TwitterSearch`` or ``easy_install TwitterSearch``. If you'd like to work with bleeding edge versions you're free to clone the ``devel`` branch. A manual installation can be done doing by downloading or cloning the repository and running ``python setup.py install``.

Search Twitter
##############

Everybody knows how much work it is to study at a university. So why not take a small shortcut? So in this example we assume we would like to find out how to copy a doctorate thesis in Germany. Let's have a look what the Twitter users have to say about `Mr Guttenberg <http://www.bbc.co.uk/news/world-europe-12608083>`_.

.. code-block:: python

    from TwitterSearch import *
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(['Guttenberg', 'Doktorarbeit']) # let's define all words we would like to have a look for
        tso.set_language('de') # we want to see German tweets only
        tso.set_include_entities(False) # and don't give us all those entity information
        
        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = 'aaabbb',
            consumer_secret = 'cccddd',
            access_token = '111222',
            access_token_secret = '333444'
         )
        
         # this is where the fun actually starts :)
        for tweet in ts.search_tweets_iterable(tso):
            print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
        
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)


The result will be a text looking similar to this one. But as you see unfortunately there is no idea hidden in those tweets how to get your doctorate thesis without any work. Damn it!

::

    @enricozero tweeted: RT @viehdeo: Archiv: Comedy-Video: Oliver Welke parodiert “Mogelbaron” Dr. Guttenbergs Doktorarbeit (Schummel-cum-laude Pla... http://t. ...
    @schlagworte tweeted: "Erst letztens habe ich in meiner Doktorarbeit Guttenberg zitiert." Blockflöte des Todes: http://t.co/pCzIn429
    @nkoni7 tweeted: Familien sind auch betroffen wenn schlechte Politik gemacht wird. Nicht nur wenn Guttenberg seine Doktorarbeit fälscht ! #absolutemehrheit

Access User Timelines
#####################

You're thinking that the global wisdom of Twitter is way too much for your needs? Well, let's query a timeline of a certain user than:

.. code-block:: python

    from TwitterSearch import *

    try:
        tuo = TwitterUserOrder('NeinQuarterly') # create a TwitterUserOrder

        # it's about time to create TwitterSearch object again
        ts = TwitterSearch(
            consumer_key = 'aaabbb',
            consumer_secret = 'cccddd',
            access_token = '111222',
            access_token_secret = '333444'
        )
        
        # start asking Twitter about the timeline
        for tweet in ts.search_tweets_iterable(tuo): 
            print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

    except TwitterSearchException as e: # catch all those ugly errors
        print(e)

You may guess the resulting output, but here it is anyway:

::

    @NeinQuarterly tweeted: To make a long story short: Twitter.
    @NeinQuarterly tweeted: A German subordinating conjunction walks into a bar. Three hours later it's joined by a verb.
    @NeinQuarterly tweeted: Foucault walks into a bar. No one notices.
    @NeinQuarterly tweeted: If it's not deleted, probably wasn't worth writing.
    @NeinQuarterly tweeted: Trust me: German prepositions aren't laughing with you. They're laughing at you.
    @NeinQuarterly tweeted: Another beautiful day for cultural pessimism.
    @NeinQuarterly tweeted: Excuse me, sir. Your Zeitgeist has arrived.

Interested in some more details?
################################

If you'd like to get more information about how TwitterSearch works internally and how to use it with all it's possibilities have a look at the `latest documentation <https://twittersearch.readthedocs.org/en/latest/>`_. A `changelog <https://github.com/ckoepp/TwitterSearch/blob/master/CHANGELOG.rst>`_ is also available within this repository.

Updating to 1.0.0 and newer
###########################

If you're upgrading from a version **< 1.0.0** be aware that the API changed! As part of the process to obtain `PEP-8 <http://legacy.python.org/dev/peps/pep-0008/>`_ compatibility all methods had to be renamed. The code changes to support the PEP-8 naming scheme are trivial. Just change the old method naming scheme from ``setKeywords(...)`` to the new one of ``set_keywords(...)``.

Apart from this issue, four other API changes were introduced with version 1.0.0:

* simplified proxy functionality (no usage of dicts but plain strings as only HTTPS proxies can be supported anyway)
* simplified geo-code parameter (``TwitterSearchOrder.set_geocode(...,metric=True)`` renamed to ``set_geocode(...,imperial_metric=True)``)
* simplified ``TwitterSearch.get_statistics()`` from dict to tuple style (``{'queries':<int>, 'tweets':<int>}`` to ``(<int>,<int>)``)
* additional feature: timelines of users can now be accessed using the new class ``TwitterUserOrder``

In total those changes can be done quickly without browsing the documentation.

If you're unable apply those changes, you might consider using TwitterSearch versions < 1.0.0. Those will stay available through pypi and therefore will be installable in the future using the common installation methods like ``pip install -I TwitterSearch==0.78.6``. Using the `release tags <https://github.com/ckoepp/TwitterSearch/releases>`_ is another easy way to navigate through all versions of this library.

License (MIT)
#############

Copyright (C) 2013 Christian Koepp

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
