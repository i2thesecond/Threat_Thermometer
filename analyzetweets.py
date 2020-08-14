import IPython
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ThreatThermometer.settings")
django.setup()
from threatthermometer.models import Tweet, TweetFrequency, ThermometerResults, MovingAverages
from django.utils import timezone
import datetime

import nltk, re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
import json

#analyze process.
#filter tweets with classifier and model

analyzeList = []
#read the analyzeList from a file. Iterate each line and count frequency of captured tweets (possibly error handling if doesnt exist in database)
totalFreq = 0

termList = []

with open('TermList.txt', 'r') as f:
	for term in f:
		term_s = term.strip()
		termList.append(term_s)
termList.append("allterms")

#clear all data that is not in TermList
termsdb = TweetFrequency.objects.values('term').distinct()
#using the term values from captured frequencies means that any term in filterlist not captured will be deleted.
for t in termsdb:
	term_s = t['term'].strip()
	if term_s not in termList:
		if term_s != "allterms":
			TweetFrequency.objects.filter(term=term_s).delete()
			Tweet.objects.filter(term=term_s).delete()
			ThermometerResults.objects.filter(term=term_s).delete()
			MovingAverages.objects.filter(term=term_s).delete()

#count frequency of terms
totalFreq = 0
for term in termList:
	if term != "allterms":
		current_time = timezone.now()
		tweets = Tweet.objects.filter(created_at__range=((current_time - datetime.timedelta(hours=1)), current_time), term=term)
		tweetFreq = len(tweets)
		freq = TweetFrequency(term=term, frequency = tweetFreq)
		freq.save()
		#count only unique tweets
		for tweet in tweets:
			if tweet.unique == True:
				totalFreq += 1
#save total tweet frequency
freqall = TweetFrequency(term="allterms", frequency=totalFreq)
freqall.save()


#calculate moving average

for term in termList:

	#create a moving average for the term if doesn't exist
	if MovingAverages.objects.filter(term=term).exists() == False:
		MovingAverages(term=term).save()
	#create a thermometer results for the term if doesn't exist
	if ThermometerResults.objects.filter(term=term).exists() == False:
		ThermometerResults(term=term).save()
	#grab the last moving average
	moving_average = MovingAverages.objects.filter(term=term)[0]
	last_average = moving_average.current_average
	#grab the freq counts
	

	tweetFreq = TweetFrequency.objects.filter(term=term).order_by('-created_at')[0]
	#twitterFreq = TwitterFrequency.objects.all()[0]
	weightedFreq = tweetFreq.frequency #/ twitterFreq.frequency

	#calculate new moving average
	new_moving_average = weightedFreq
	new_moving_period = 1
	new_moving_average = (weightedFreq + (last_average * moving_average.periods)) / (moving_average.periods + 1)
	new_moving_period = (moving_average.periods + 1)
	#update the moving average
	moving_average.current_average = new_moving_average
	moving_average.periods = new_moving_period
	moving_average.save()
	
	term_result = 2
	if last_average != 0:
		percentage_change =  float(new_moving_average - last_average) / last_average
		if float(percentage_change) > 0.30:
			term_result = 4
		elif float(percentage_change) <= 0.30 and float(percentage_change) > 0.10:
			term_result = 3
		elif float(percentage_change) <= 0.10 and float(percentage_change) >= -0.10:
			term_result = 2
		elif float(percentage_change) < -0.10 and float(percentage_change) >= -0.30:
			term_result = 1
		elif float(percentage_change) < -0.30:
			term_result = 0
	update_result = ThermometerResults.objects.filter(term=term).get()
	update_result.ranking = term_result
	update_result.save()



#detect trends associated with the term

#remove url
allTokens = []
default_stopwords = set(nltk.corpus.stopwords.words('english'))
ENGLISH_RE = re.compile(r'[a-z]+')

def processTokens(tokens):
	# Lowercase all words (default_stopwords are lowercase too)
	tokens = [word.lower() for word in tokens]
	# Remove single-character tokens (mostly punctuation)
	tokens = [word for word in tokens if len(word) > 1]
	# Remove numbers
	tokens = [word for word in tokens if not word.isnumeric()]
	lmtzr = nltk.WordNetLemmatizer()
	# Save the list between tokens
	lemmatized = []
	for word in tokens:
		# Check english terms
		if not ENGLISH_RE.match(word):
			continue
		# Check stopwords
		if word in default_stopwords:
			continue
		lemmatized.append(lmtzr.lemmatize(word))
	return lemmatized

for term in termList:
	if term != "allterms":
		tweets = Tweet.objects.filter(term=term)
		termsTweets = []
		for tweet in tweets:
			termsTweets.append(tweet.text)
		tokens = []
		for tweet in termsTweets:
			tokens.extend(nltk.word_tokenize(tweet))
		#returns a frequency distribution
		tokens = processTokens(tokens)
		allTokens.extend(tokens)
		fdist = nltk.FreqDist(tokens)
		trending = fdist.most_common(10)
		trending = json.dumps(trending)
		results = ThermometerResults.objects.filter(term=term).get()
		results.trending_keywords = trending
		results.save()
#then process for allterms
fdist = nltk.FreqDist(allTokens)
trending = fdist.most_common(10)
trending = json.dumps(trending)
results = ThermometerResults.objects.filter(term="allterms").get()
results.trending_keywords = trending
results.save()


#option for more classifiers

#remove anything older than 7 days
current_time = timezone.now()
keepTweetFreq = TweetFrequency.objects.filter(created_at__range=((current_time - datetime.timedelta(days=7)), current_time)).values_list("id", flat=True)  # only retrieve ids
TweetFrequency.objects.exclude(pk__in=list(keepTweetFreq)).delete()

keepTweets = Tweet.objects.filter(created_at__range=((current_time - datetime.timedelta(days=7)), current_time)).values_list("id", flat=True)  # only retrieve ids
Tweet.objects.exclude(pk__in=list(keepTweets)).delete()
