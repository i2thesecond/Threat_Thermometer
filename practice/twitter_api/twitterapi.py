from nltk.twitter import Query, Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile
from pprint import pprint


#tw.tweets(keywords='FANG', limit=10) #sample from the public stream
#tw.tweets(follow=['759251', '612473'], limit=10) # see what CNN and BBC are talking about

oauth = credsfromfile()



client = Streamer(**oauth)

userids = ['2820445494']

client.register(TweetViewer(limit=10))
client.statuses.filter(follow=userids)

