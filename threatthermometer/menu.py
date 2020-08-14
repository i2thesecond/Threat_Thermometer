from .models import ThermometerResults

def nav_menu(request):
	
	link_menu = ThermometerResults.objects.order_by('term')

	return {'link_menu': link_menu}
