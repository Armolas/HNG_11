from django.http import JsonResponse
import requests

# Create your views here.
def hello(request):
    weather_url = 'https://api.weatherapi.com/v1/current.json?key=cd438e8673764765b7760027240207&q=auto:ip'
    weather_response = requests.get(weather_url).json()
    city = weather_response.get('location').get('name')
    temp = weather_response.get('current').get('temp_c')
    name = request.GET.get('visitor_name')
    ip = request.META.get('REMOTE_ADDR')
    response = {
            'client_ip': ip,
            'location': city,
            'greeting': f'Hello, {name}!, the temperature is {temp} degrees Celcius in {city}'
            }
    return JsonResponse(response)


