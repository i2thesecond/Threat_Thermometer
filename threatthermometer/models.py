from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

#key
class ThermometerResults(models.Model):
	term = models.CharField(max_length = 20)
	ranking = models.IntegerField(
		default=2,
		validators=[MaxValueValidator(4), MinValueValidator(0)]
     )
     #add field for "trend keywords", which is essentially just a frequency count
	def __str__(self):
		return str(self.term)
		
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
	frequency = models.IntegerField()
	def __str__(self):
		return str(self.term + " frequency on " + str(self.created_at))
