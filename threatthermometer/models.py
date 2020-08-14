from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MaxValueValidator, MinValueValidator

#key
class ThermometerResults(models.Model):
	term = models.CharField(max_length = 20)
	ranking = models.IntegerField(
		default=2,
		validators=[MaxValueValidator(4), MinValueValidator(0)]
	)
     #add field for "trend keywords", which is essentially just a frequency count
	trending_keywords = JSONField(default="", blank=True)
	def __str__(self):
		return str(self.term)
		
class MovingAverages(models.Model):
	term = models.CharField(max_length = 20)
	current_average = models.IntegerField(default=0)
	periods = models.IntegerField(default=0)
	def __str__(self):
		return str("Moving Average " + self.term + " " + str(self.current_average))

#key		
class Tweet(models.Model):
	created_at = models.DateTimeField()
	text = models.CharField(max_length=1000) #is there a default max length or am i needlessly complicating this?
	retweeted = models.BooleanField()
	hashtags = ArrayField(models.CharField(max_length=360, blank=True))
	#'unique' checks to make sure double filter terms don't get counted as a seperate tweet
	unique = models.BooleanField(default=True)
	term = models.CharField(max_length=30, default="cybersecurity")
	def __str__(self):
		return str("Tweet " + str(self.created_at))
		
		
#key 
class TweetFrequency(models.Model):
	term = models.CharField(max_length = 20)
	created_at = models.DateTimeField(auto_now_add=True)
	frequency = models.IntegerField(default=0)
	def __str__(self):
		return str(self.term + " frequency on " + str(self.created_at))
'''
#keeps track of total tweets per analyze.py session. I didn't want to make a seperate table for this but I couldn't think of another way to track the frequency.
class TwitterFrequency(models.Model):
	frequency = models.IntegerField(default=0)
	def __str__(self):
		return str("Total twitter tweets " + str(self.frequency))
'''
