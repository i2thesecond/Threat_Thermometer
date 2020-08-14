import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import json
import time
from datetime import datetime
from dateutil.parser import parse
import pprint
import nltk
import IPython
import os
import django
#connect to Django model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ThreatThermometer.settings")
django.setup()
# your imports, e.g. Django models
from threatthermometer.models import Tweet



# Tweepy class to access Twitter API
class MyStreamListener(tweepy.StreamListener):
	
	def on_status(self, status):
		print(status.text)
		
	def on_connect(self):
		print("You are connected to the Twitter API")

	def on_error(self, status_code):
		if status_code == 420:
			print("Rate limit disconnect")
			return False
		if status_code != 200:
			print("Connection Error")
			# returning false disconnects the stream
			return False
	
	def on_data(self,data):
		
		try:
			'''
			#increment the total twitter frequency table by 1 per each tweet captured
			if ThermometerResults.objects.all.exists() == False:
				twitterFreq = TwitterFrequency()
				twitterFreq.frequency = 1
				twitterFreq.save()
			else:
				twitterFreq = TwitterFrequency.objects.all()[:1]
				twitterFreq.frequency += 1
				twitterFreq.update()
			'''
			#create a dictionary type
			tweet_data = json.loads(data)
			
			tweet = Tweet()
			tweet.created_at = parse(tweet_data['created_at'])
			tweet.retweeted = tweet_data['retweeted']
			tweet.hashtags = []
			try:
				#if 'quoted_status' in tweet_data and 'extended_tweet' in tweet_data['quoted_status']:
				#need to add logic to capture both quoted_status and the normal tweet.
				if 'retweeted_status' in tweet_data and 'extended_tweet' in tweet_data['retweeted_status']:
					tweet.text = tweet_data['retweeted_status']['extended_tweet']['full_text']
					for e in tweet_data['retweeted_status']['extended_tweet']['entities']['hashtags']:
						tweet.hashtags.append(e['text'])
				elif 'extended_tweet' in tweet_data:
					tweet.text = tweet_data['extended_tweet']['full_text']
					for e in tweet_data['extended_tweet']['entities']['hashtags']:
						tweet.hashtags.append(e['text'])
				else:
					tweet.text = tweet_data['text']
					for e in tweet_data['entities']['hashtags']:
						tweet.hashtags.append(e['text'])
			except AttributeError:
				print('attribute error: ' + tweet_data)
				
			#IPython.embed()
				
			if len(tweet.text) > 1000:
				IPython.embed()
			
			#tokenize. unsure how twipper api does the matching, doing so manually
			tokenized_text = nltk.word_tokenize(tweet.text)
			tokenized_lower_text = [w.lower() for w in tokenized_text]
			lower_hashtags = [w.lower() for w in tweet.hashtags]
			#mark the terms
			
			tweet.unique = True
			saved = False
			for term in filterList:
				if (term in tokenized_lower_text):
						tweet.term = term
						tweet.save()
						print("Saved Tweet as " + term + "\n")
						saved = True
						if tweet.unique == True:
							tweet.unique = False
				elif (term in lower_hashtags):
						tweet.term = term
						tweet.save()
						print("Saved Tweet as " + term + "\n")
						saved = True
						if tweet.unique == True:
							tweet.unique = False
			#if saved == False:
				#IPython.embed()
				#implement quoted status by making a new model field called 'quoted_status' and 'quoted_text'.
				#look at original tweet for a match, if not found, look at the quoted text for a match. 
				#later will have to find a way to process the tweet and the quoted tweet as one tweet. 
			
			'''if 'text' in tweet_data:
				
				created_at = tweet_data['created_at']
				tweet_text = tweet_data['text']
				#hashtags = tweet_data['entities']['hashtags']
				#retweeted = tweet_data['retweeted']
				print(created_at)
				print('\n')
				print(tweet_text)
				print('\n')'''	
				
				

		except Error as e:
			print(e)


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
	


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

filterList = []
#read the filterList from a file. 

with open('TermList.txt', 'r') as f:
    for line in f:
        filterList.append(line.strip())

#write diagram and documents to the whole process. 

myStream.filter(track=filterList, is_async=True)
