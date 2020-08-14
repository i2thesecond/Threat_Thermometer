from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
import json
import IPython
from .models import ThermometerResults, TweetFrequency

# Create your views here.

def index(request):
	return render(request, 'threatthermometer/index.html')

def results(request, term):

	try:
		queryitem = ThermometerResults.objects.filter(term=term).get()
		trending = json.loads(queryitem.trending_keywords)
	except ThermometerResults.DoesNotExist:
		trending = []
	trending_keywords = {'trending': trending}
	context = {'term': term, 'trending': trending} 	
	return render(request, 'threatthermometer/results.html', context)

#aggregate the data the return a JSON response with the labels and data.

def result_chart(request, term):
	labels = []
	data = []
	try:
		queryset = ThermometerResults.objects.filter(term=term)
		for entry in queryset:
			labels.append(entry.term)
			data.append(entry.ranking)
	except ThermometerResults.DoesNotExist:
		labels.append("Does Not Exist")
		data.append(0)
	return JsonResponse(data={'labels': labels,'data': data,})

def frequency_chart(request, term):
	labels = []
	data = []
	try:
		#select the first 7 entries (1 per each day).
		queryset = TweetFrequency.objects.filter(term=term).order_by('-created_at')[:7]
		for entry in queryset:
			labels.append(entry.created_at.strftime('%Y-%m-%d'))
			data.append(entry.frequency)
	except TweetFrequency.DoesNotExist:
		labels.append("Does Not Exist")
		data.append(0)
	return JsonResponse(data={'labels': labels,'data': data,})
