TwitterSearch
=============

*TwitterSearch* was (and still is) developed as part of a project about social media at the `Carl von Linde-Akademie <http://www.cvl-a.tum.de/>`_ which is part of the `Technische Universität München <https://www.tum.de>`_. Thus it is a data collecting toolkit and **not implementing** the whole Twitter API but the `Search API <https://dev.twitter.com/docs/api/1.1/get/search/tweets>`_.

It's using the REST API in **version 1.1** only. In it's recent version it directly uses IDs of tweets to navigate throughout the available tweets instead of pages, which is way more comfortable to use and more convenient for really getting all possible tweets.

Also *TwitterSearch* is build to be highly flexible in its usage making it usable even within exotic use-cases. Details about non-default use-cases can be found in the *Advanced usage* sections within the class articles.

Architecture
============

TwitterSearch consists of three classes: `TwitterSearch <TwitterSearch.html>`_, `TwitterSearchOrder <TwitterSearchOrder.html>`_ and `TwitterSearchException <TwitterSearchException.html>`_.

Table of contents
=================

.. toctree::
   :maxdepth: 2

   basic_usage
   TwitterSearch
   TwitterSearchOrder
   TwitterSearchException

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Contribution
============

Feel free to open issues, submit code or fork.
