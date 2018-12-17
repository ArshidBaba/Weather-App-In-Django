from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
	# url = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=c11610db0b77c709dcd77c0ebb760793'
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=c11610db0b77c709dcd77c0ebb760793'

	if request.method == 'POST':
		form = CityForm(request.POST)
		form.save()

	form = CityForm()

	cities = City.objects.all()

	weather_data = []

	for city in cities:

		r = requests.get(url.format(city)).json()

		city_weather = {
			'city': city.name,
			'temperature': (r['main']['temp'])-273.15,
			'description': r['weather'][0]['description'],
			'icon': r['weather'][0]['icon'],
		}

		weather_data.append(city_weather)

	#print(weather_data)
	context = {'weather_data': weather_data, 'form': form}
	return render(request, 'weather/weather.html', context)
