from django.contrib import admin

# Register your models here.

from .models import Tweet, ThermometerResults, TweetFrequency

admin.site.register(Tweet)
admin.site.register(ThermometerResults)
admin.site.register(TweetFrequency)
