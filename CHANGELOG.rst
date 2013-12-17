Change history
**************

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
