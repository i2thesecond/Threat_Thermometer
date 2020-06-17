from twitter_scraper import get_tweets


'''
tweetId	string	Tweet's identifier, visit twitter.com/USERNAME/ID to view tweet.
userId	string	Tweet's userId
username	string	Tweet's username
tweetUrl	string	Tweet's URL
isRetweet	boolean	True if it is a retweet, False otherwise
isPinned	boolean	True if it is a pinned tweet, False otherwise
time	datetime	Published date of tweet
text	string	Content of tweet
replies	integer	Replies count of tweet
retweets	integer	Retweet count of tweet
likes	integer	Like count of tweet
entries	dictionary	Has hashtags, videos, photos, urls keys. Each one's value is list
'''

for tweet in get_tweets('cyber', pages=1):
    if (tweet['isRetweet']==False):
        print('isRetweet ', tweet['isRetweet'])
        print('userID: ' + tweet['username'] + '\n')
        print('time ', tweet['time'])
        print('tweet ' + tweet['text'] + '\n')
        print('entries ', tweet['entries']['hashtags'])
        print('\n\n')
