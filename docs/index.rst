TwitterSearch
=============

*TwitterSearch* was developed as part of a project about social media at the `Carl von Linde-Akademie <http://www.cvl-a.tum.de/>`_, an institution of the `Technische Universität München <https://www.tum.de>`_. Thus, *TwitterSearch* is a data collecting toolkit and is **not implementing** the whole Twitter API but the `Search API <https://dev.twitter.com/docs/api/1.1/get/search/tweets>`_ and the `User Timeline API <https://dev.twitter.com/rest/reference/get/statuses/user_timeline>`_. The library is fully accessible through the `official repository <https://www.github.com/ckoepp/TwitterSearch/>`_ at github and maintained by Christian Koepp.

*TwitterSearch* is using the REST API in **version 1.1** only. In its recent version, the library is using identifiers of tweets to navigate throughout the available list of tweets. Doing so enables a more flexible and efficient iteration than the traditional method of using pages. Also, *TwitterSearch* is build to be highly flexible in its usage making it usable even within exotic use-cases. Details about non-default use-cases can be found in the *Advanced usage* sections within the class articles of this documentation.

All classes and their methods are tested against the latest Python 2 and Python 3 versions automatically. The current state of all branches is visible through `Travis CI <https://travis-ci.org/ckoepp/TwitterSearch/branches>`_. Additionally, you should note that with version 1.0 and upwards `PEP-8 <http://legacy.python.org/dev/peps/pep-0008/>`_ compatibility is enforced. Those checks were done by running the `pep8` toolkit. If you're interested in contributing to *TwitterSearch* make sure your patches are PEP-8 compatible. Additionally, patches are required to not break the current test cases and to bring test cases with them to test new features and functionalities.

The history of commits and changes of this library can be either accessed by using the `official github repository <https://www.github.com/ckoepp/TwitterSearch/>`_ . Also, a summary of the major changes is provided within the ``CHANGELOG.rst`` file of the package.

.. warning::
    If you're upgrading from a version < 1.0.0 be aware that the API changed! To support PEP-8 completely, former methods named ``someMethod()`` were renamed to ``some_method()``. Apart from this issue, four other API changes were introduced with version 1.0.0:

    * simplified proxy functionality: no usage of dicts but plain strings as only HTTPS proxies can be supported
    * simplified geo-code parameter: ``TwitterSearchOrder.set_geocode(...,metric=True)`` renamed to ``set_geocode(...,imperial_metric=True)``
    * simplified ``TwitterSearch.get_statistics()``: switched from dict to tuple style (``{'queries':<int>, 'tweets':<int>}`` to ``(<int>,<int>)``)
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