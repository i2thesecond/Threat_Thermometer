from django.contrib import admin

# Register your models here.

from .models import Tweet, ThermometerResults, TweetFrequency, MovingAverages

admin.site.register(Tweet)
admin.site.register(ThermometerResults)
admin.site.register(TweetFrequency)
admin.site.register(MovingAverages)
