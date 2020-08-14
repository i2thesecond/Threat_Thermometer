import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import json
import time
from datetime import datetime
from dateutil.parser import parse
import pprint
import IPython
import os
import pandas

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""


def getAllTweets(screen_name):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	# test authentication
	# If the authentication was successful, you should
	# see the name of the account print out
	try:
		api.verify_credentials()
		print("Authentication OK")
	except:
		print("Error during authentication")
	
	alltweets = []
	newtweets = api.user_timeline(screen_name = screen_name, count=200, tweet_mode='extended')
	alltweets.extend(newtweets)
	
    #save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(newtweets) > 0:
		print(f"getting tweets before {oldest}")

        #all subsiquent requests use the max_id param to prevent duplicates
		newtweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
        #save most recent tweets
		alltweets.extend(newtweets)
		
        #update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print(f"...{len(alltweets)} tweets downloaded so far")
	
	outtweets = []
	for tweet in alltweets:
		#transform the tweepy tweets into a list of dictionary objects containing the full text.
		try:
			outtweets.append({"user":tweet.id_str, "created_at":tweet.created_at, "text":tweet.full_text})
		except AttributeError:
			try:
				outtweets.append({"user":tweet.id_str, "created_at":tweet.created_at, "text":tweet.text})
			except AttributeError:
				print("Atttribute Error when trying to extract text from Status object.\n")
	return outtweets


userAccounts = []
#read the userAccounts list from a file. 

with open('users.txt', 'r') as f:
    for line in f:
        userAccounts.append(line)

tweetCorpus = []

for user in userAccounts:
	tweetCorpus.extend(getAllTweets(user))
	print(len(tweetCorpus))

IPython.embed()
dataframe = pandas.DataFrame.from_dict(tweetCorpus, orient="index")
dataframe.to_csv("tweetCorpus.csv")
