TwitterSearch
-------------
This library allows you easily create a search through the Twitter Search API without having to know about the API details. Based on such a search you can even iterate throughout all tweets reachable via the Twitter Search API. There is an automatic reload of the next pages while using the iteration.

Example usage
-------------
The library is still in a very early stage. However, if you would like to use it we prepared a small example about how to play around with it.

```python
try:
    tso = TwitterSearchOrder()
    tso.setKeywords(['Guttenberg', 'Doktorarbeit']) # we do want to look for tweets including those words
    tso.setLanguage('de') # we do need German tweets only
    tso.setCount(102) # this is already the default value
    tso.setIncludeEntities(False) # default value, too :)

    tb = TwitterSearch(
        consumer_key = 'aaabbb',
        consumer_secret = 'cccddd',
        access_token = '111222',
        access_token_secret = '333444'
     )

    tb.authenticate()

    counter  = 0
    for tweet in tb.searchTweetsIterable(tso):
        counter += 1
        print '@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text'])
     print 'Found a total of %i tweets' % counter   

except TwitterSearchException, e:
    print e.msg
```
