Change history
**************

1.0.1
#####

* added support for user-defined callback-method while performing API queries (issue #25)
* added support for advanced query operators (issue #24)
* adjusted search term parsing in method TwitterSearchOrder.set_search_url()
* auto-handling of keywords with spaces

1.0.0
#####

* PEP-8 compatible API (issue #12)
* added support of loading timelines of users
* simplified proxy functionality (no usage of dicts but plain strings)
* simplified geo-code parameter (``TwitterSearchOrder.set_geocode(...,metric=True)`` renamed to ``set_geocode(...,imperial_metric=True)``)
* simplified ``TwitterSearch.get_statistics()`` from dict to tuple style (``{'queries':<int>, 'tweets':<int>}`` to ``(<int>,<int>)``)
* dropped Python 2.6 support (it still works, but some test cases are failing and it's just too much work to add support for 2.6 + 2.7 + 3.x)
* Full rewrite of documentation

0.78.6
######

* Fixed codec error on Win7 installation (issue #21)
* Added manual iteration support (issue #20)

0.78.5
######

* fixed proxy usage at initialization of TwitterSearch object

0.78.4
######

* fixed missing url encoding of search keywords (issue #16)
* created test to check url encoding of keywords
* fixed typo in documentation (issue #17)

0.78.3
######

* fixed a bug (issue #10): min() with lambda-function doesn't work with empty responses 

0.78.2
######

* using lambda function to determine minimal ID of tweets on reloads of new pages from API

0.78.1
######

* added interface to help/languages to load supported ISO 6391-1 language codes directly from API

0.76
####

* added tests for TwitterSearchOrder class
* Python3/Python2 improvements by using conditional expressions
* fixed url-encoding of ',' letters in geocode argument within createSearchURL()
* some internally used variables are now marked as private (e.g. TwitterSearch.__response) 
* added proxy feature (https only)
* removed TwitterSearch.isNext()
* added TwitterSearchException(1016) [Invalid dict]
* added docstrings

0.75
####

* added requirements.txt
* added license file
* added Python3 support
* changed from oauth2 and simplejson to requests and requests_oauthlib
* added verification of credentials feature
