from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

from .models import ThermometerResults, TweetFrequency

# Create your views here.

def index(request):
	#create a list that holds all the results from Thermometer Results to pass into the index page
	term_list = ThermometerResults.objects.order_by('term')
	context = {'term_list': term_list}
	return render(request, 'threatthermometer/index.html', context)
'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'term': question})
'''
def results(request, term):
	context = {'term': term}
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
		queryset = TweetFrequency.objects.filter(term=term)[:7]
		for entry in queryset:
			labels.append(entry.created_at.strftime('%Y-%m-%d'))
			data.append(entry.frequency)
	except TweetFrequency.DoesNotExist:
		labels.append("Does Not Exist")
		data.append(0)
	return JsonResponse(data={'labels': labels,'data': data,})
