from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('results/<str:term>/', views.results, name='results'),
    #seperating graph view by url view
    #result chart
    path('result-chart/<str:term>', views.result_chart, name='result-chart'),
	#frequency chart
    path('frequency-chart/<str:term>', views.frequency_chart, name='frequency-chart'),
]
