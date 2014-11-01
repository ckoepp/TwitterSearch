TwitterSearch
=============

*TwitterSearch* was developed as part of a project about social media at the `Carl von Linde-Akademie <http://www.cvl-a.tum.de/>`_ which is part of the `Technische Universität München <https://www.tum.de>`_. Thus, it is a data collecting toolkit and **not implementing** the whole Twitter API but the `Search API <https://dev.twitter.com/docs/api/1.1/get/search/tweets>`_ and the `User Timeline API <https://dev.twitter.com/rest/reference/get/statuses/user_timeline>`_. 

The library is fully accessible through the `official repository <https://www.github.com/ckoepp/TwitterSearch/>`_ at github and maintained by Christian Koepp.

It's using the REST API in **version 1.1** only. In its recent version it directly uses IDs of tweets to navigate throughout the available tweets instead of pages, which is way more comfortable to use and more convenient for really getting all possible tweets. Also, *TwitterSearch* is build to be highly flexible in its usage making it usable even within exotic use-cases. Details about non-default use-cases can be found in the *Advanced usage* sections within the class articles.

All classes and functionality is tested against the latest Python 2 and Python 3 versions automatically. The current state of all branches is visible through `Travis CI <https://travis-ci.org/ckoepp/TwitterSearch/branches>`_. Additionally, you should note that with version 1.0 and upwards `PEP-8 <http://legacy.python.org/dev/peps/pep-0008/>`_ compatibility is enforced. Checks are done by running the `pep8` toolkit.

The history of changes can be either accessed by using the `official github repository <https://www.github.com/ckoepp/TwitterSearch/>`_ or by looking at summary outlined as in the ``CHANGELOG.rst`` file within the package.

.. warning::
    If you're upgrading from a version < 1.0.0 be aware that the API changed! To support PEP-8 completely, former methods named ``someMethod()`` are now accessible as ``some_method()``. Apart from this issue, four other API changes were introduced with version 1.0.0:

    * simplified proxy functionality (no usage of dicts but plain strings as only HTTPS proxies can be supported)
    * simplified geo-code parameter (``TwitterSearchOrder.set_geocode(...,metric=True)`` renamed to ``set_geocode(...,imperial_metric=True)``)
    * simplified ``TwitterSearch.get_statistics()`` from dict to tuple style (``{'queries':<int>, 'tweets':<int>}`` to ``(<int>,<int>)``)
    * additional feature: timelines of users can now be accessed using the new class :class:`TwitterUserOrder`

    In total those changes can be done quickly without browsing this documentation. If you are not able to do those changes just keep using the versions < 1.0.0. Those will stay available through pypi and therefore will be installable in the future using the common installation methods.


Table of contents
=================

.. toctree::
   :maxdepth: 2

   basic_usage
   modules
   advanced_usage_ts
   advanced_usage_tse
   advanced_usage_tso
   advanced_usage_tuo

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Contribution
============

Feel free to open issues, submit code or fork.