from django.apps import AppConfig 
import os
import subprocess

class ThreatThermometerConfig(AppConfig):
	name = 'threatthermometer'
	verbose_name = "Threat Thermometer"
	def ready(self):
		print(os. getcwd())
		'''
		try:
			#subprocess.run(['false'], check=True)
			subprocess.run(['python3','TwitterStreamer/twitterstreamer.py'])
		except subprocess.CalledProcessError as err:
			print('ERROR:', err)'''
