import IPython
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ThreatThermometer.settings")
django.setup()
from threatthermometer.models import Tweet, TweetFrequency, ThermometerResults
from django.utils import timezone
import datetime

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

for t in termsdb:
	term_s = t['term'].strip()
	if term_s not in termList:
			TweetFrequency.objects.filter(term=term_s).delete()
			Tweet.objects.filter(term=term_s).delete()
			ThermometerResults.objects.filter(term=term_s).delete()


#count frequency of terms
totalFreq = 0
for term in termList:
	current_time = timezone.now()
	tweets = Tweet.objects.filter(created_at__range=((current_time - datetime.timedelta(hours=1)), current_time), term=term)
	freq = TweetFrequency(term=term, frequency=len(tweets))
	freq.save()
	#count only unique tweets
	for tweet in tweets:
		if tweet.unique == True:
			totalFreq += 1
#save total tweet frequency
freqall = TweetFrequency(term="allterms", frequency=totalFreq)
freqall.save()

for term in termList:
	if ThermometerResults.objects.filter(term=term).exists() == True:
		tweet_result = ThermometerResults.objects.filter(term=term)
		tweet_result.ranking = 2
		tweet_result.update()
	else:
		tweet_result = ThermometerResults()
		tweet_result.term = term
		tweet_result.ranking = 2
		tweet_result.save()


#remove anything older than 7 days
current_time = timezone.now()
keepTweetFreq = TweetFrequency.objects.filter(created_at__range=((current_time - datetime.timedelta(days=7)), current_time)).values_list("id", flat=True)  # only retrieve ids
TweetFrequency.objects.exclude(pk__in=list(keepTweetFreq)).delete()

keepTweets = Tweet.objects.filter(created_at__range=((current_time - datetime.timedelta(days=7)), current_time)).values_list("id", flat=True)  # only retrieve ids
Tweet.objects.exclude(pk__in=list(keepTweets)).delete()
