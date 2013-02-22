# TwitterSearch
This library allows you easily create a search through the Twitter Search API without having to know too much about the API details. Based on such a search you can even iterate throughout all tweets reachable via the Twitter Search API. There is an automatic reload of the next pages while using the iteration.

## Reasons to use TwitterSearch
Well, because it can be quite annoying to always parse the search url together and a minor spelling mistake is sometimes hard to find. Not to mention the pain of getting the next page of the results. Why not centralize this process and concentrate on the more important parts of the project?

More than that, TwitterSearch is:
 * pretty small (around 300 lines of code currently)
 * pretty easy to use, even for beginners
 * pretty iterable without any need to manually reload more results from the API
 * pretty wrong values of API arguments are to raise an exception. This is done before the API gets queried and therefore helps to avoid to reach Twitters' limitations by totally wrong API calls
 * pretty pretty to look at :)

## Example
The library is still in a very early stage. However, if you would like to use it we prepared a small example about how to play around. 

Everybody knows how much work it is to study at a university. So why not take a small shortcut? So in this example we assume we would like to find out how to copy a doctorate thesis in Germany. Let's have a look what the Twitter users have to say about [Mr Guttenberg](http://www.bbc.co.uk/news/world-europe-12608083).

```python
from TwitterSearch import *
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.setKeywords(['Guttenberg', 'Doktorarbeit']) # let's define all words we would like to have a look for
    tso.setLanguage('de') # we want to see German tweets only
    tso.setCount(100) # please dear Mr Twitter, give us 100 results per page (this is the default value, I know :P)
    tso.setIncludeEntities(False) # and don't give us all those entity information (this is a default value too)

    # it's about time to create a TwitterSearch object with out secret tokens
    tb = TwitterSearch(
        consumer_key = 'aaabbb',
        consumer_secret = 'cccddd',
        access_token = '111222',
        access_token_secret = '333444'
     )

    tb.authenticate() # we need to use the oauth authentication first to be able to sign messages

    counter  = 0 # just a small counter
    for tweet in tb.searchTweetsIterable(tso): # this is where the fun actually starts :)
        counter += 1
        print '@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text'])

     print '*** Found a total of %i tweets' % counter   

except TwitterSearchException, e: # take care of all those ugly errors if there are some
    print e.message
```
