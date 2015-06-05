
Advanced usage: The :class:`TwitterSearchException` class
=========================================================

It is possible to print an *TwitterSearch* exception. Doing so will result in strings of the type ``Error <TwitterSearchException.code>: <TwitterSearchException.message>``. For those new to Python, the standard way to print an exceptions is:

.. code-block:: python

    except TwitterSearchException as e:
        print(e)

List of exceptions
------------------

There are *two* different kinds of exceptions in *TwitterSearch*. The first kind is based on the HTTP status of the query to the Twitter API while the second type of exceptions are based on misconfiguration of the library. Misconfiguration can be performed, for example, by setting odd parameters or trying to access tweets without querying the API before.

Library based exceptions
++++++++++++++++++++++++

All exceptions based on issues within TwitterSearch do have ``TwitterSearchException.code >= 1000``.

====== ======================================
*Code* *Message*                             
------ --------------------------------------
1000   Neither a list nor a string            
------ --------------------------------------
1001   Not a list object                     
------ --------------------------------------
1002   No ISO 6391-1 language code           
------ --------------------------------------
1003   No valid result type                  
------ --------------------------------------
1004   Invalid number                         
------ --------------------------------------
1005   Invalid unit                           
------ --------------------------------------
1006   Invalid callback string               
------ --------------------------------------
1007   Not a date object                     
------ --------------------------------------
1008   Invalid boolean                       
------ --------------------------------------
1009   Invalid string                        
------ -------------------------------------- 
1010   Not a valid TwitterSearchOrder object
------ --------------------------------------
1011   No more results available              
------ --------------------------------------
1012   No meta data available                
------ --------------------------------------
1013   No tweets available                   
------ --------------------------------------
1014   No results available                   
------ --------------------------------------
1015   No keywords given                      
------ --------------------------------------
1016   Invalid dict                           
------ --------------------------------------
1017   Invalid user id or screen-name
------ --------------------------------------
1018   Not a callable function
====== ======================================

HTTP based exceptions
+++++++++++++++++++++

Exceptions based on the `HTTP status response <https://dev.twitter.com/docs/error-codes-responses>`_ of the Twitter API are ``TwitterSearchException.code < 1000``. Note that the ``code`` attribute is exactly the HTTP status value returned to *TwitterSearch* from the Twitter API. All those exceptions are raised in :class:`TwitterSearch` only.

====== ======================================================================================================================
*Code* *Message*        
------ ----------------------------------------------------------------------------------------------------------------------
400    Bad Request: The request was invalid
------ ----------------------------------------------------------------------------------------------------------------------
401    Unauthorized: Authentication credentials were missing or incorrect
------ ----------------------------------------------------------------------------------------------------------------------
403    Forbidden: The request is understood, but it has been refused or access is not allowed
------ ----------------------------------------------------------------------------------------------------------------------
404    Not Found: The URI requested is invalid or the resource requested does not exists
------ ----------------------------------------------------------------------------------------------------------------------
406    Not Acceptable: Invalid format is specified in the request
------ ----------------------------------------------------------------------------------------------------------------------
410    Gone: This resource is gone
------ ----------------------------------------------------------------------------------------------------------------------
420    Enhance Your Calm:  You are being rate limited
------ ----------------------------------------------------------------------------------------------------------------------
422    Unprocessable Entity: Image unable to be processed
------ ----------------------------------------------------------------------------------------------------------------------
429    Too Many Requests: Request cannot be served due to the application's rate limit having been exhausted for the resource
------ ----------------------------------------------------------------------------------------------------------------------
500    Internal Server Error: Something is broken
------ ----------------------------------------------------------------------------------------------------------------------
502    Bad Gateway: Twitter is down or being upgraded
------ ----------------------------------------------------------------------------------------------------------------------
503    Service Unavailable: The Twitter servers are up, but overloaded with requests
------ ----------------------------------------------------------------------------------------------------------------------
504    Gateway timeout: The request couldn't be serviced due to some failure within our stack
====== ======================================================================================================================

Advanced exception usage
------------------------

The HTTP exceptions are somehow configurable. Imagine  there is a reason why you don't like TwitterSearch to raise an exception when a 404 HTTP status is returned by the Twitter API. Instead you'd like to raise an exception when a 200 HTTP status is returned. Maybe you would like to test your firewall by doing complex HTTP queries. Anyway, let's just assume there is some strange reason to do so...

Since TwitterSearch is designed to be used in academic and highly individual scenarios it is perfectly possible to do such crazy stuff without too much of trouble.

.. code-block:: python

  from TwitterSearch import *
  
  tso = TwitterSearchOrder()
  tso.set_keywords(['strange', 'use-case'])
  tso.set_include_entities(False)
  
  ts = TwitterSearch(
      consumer_key = 'onetwothree',
      consumer_secret = 'fourfivesix',
      access_token = 'foo',
      access_token_secret = 'bar'
  )
  
  # add a HTTP status based exception based on status 200
  ts.exceptions.update({200 : 'It worked - damn it!' })
  
  # delete exception based on HTTP status 400
  del ts.exceptions[400]
  
  try:
      ts.authenticate()
      for tweet in ts.search_tweets_iterable(tso):
          print("Seen tweed with ID %i" % tweet['id'])
  
  except TwitterSearchException as e:
      if e.code < 1000:
          print("HTTP status based exception: %i - %s" % (e.code, e.message))
      else:
        print("Regular exception: %i - %s" % (e.code, e.message))

If your credentials are correct you will receive the output ``HTTP status based exception: 200 - It worked - damn it!``.
