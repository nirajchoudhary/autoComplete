from django.shortcuts import render,redirect,render_to_response
from models import City, Airports, RailwayStation, Pincode
from django.http import HttpResponse
from django.core import serializers
#from django.utils import simplejson
import json
import requests
from time import sleep
import math

#load whole table at once into json variable
def loadData(request):
	#if request.method == "POST":
	#	source = request.POST['source']
		airports = Airports.objects.values_list('name','city').all()
		#json_airports = simplejson.dumps(airports)
		results = []
		for airport in airports:
			airport_json = {}
			#airport_json['id'] = airport.id
			airport_json['name'] = airport[0]
			airport_json['city'] = airport[1]
			results.append(airport_json)
		json_airports = simplejson.dumps(results)
		#except:
	#		pass
	#else:
		data = 'fail'
		mimetype = 'application/json'
		return render(request,'redirect.html',{"airports":json_airports})


#load data according to query into json variable
def searchView(request):
	#if request.method == "POST":
	if request.is_ajax():
		#try:
			q = request.GET.get('term', '')
			#q = request.POST.get('term')
			#cities = City.objects.filter(city__search = q + '*')			
			results = []
			if q.isdigit():
				pincodes = Pincode.objects.filter(pincode__istartswith = q )
				for pincode in pincodes:
					pincode_json = {}
					pincode_json['id'] = pincode.id
					pincode_json['label'] = pincode.officeName + ", " + pincode.Taluk + ", " + pincode.Districtname + ", " + pincode.state + ", " + pincode.pincode
					pincode_json['value'] = pincode.officeName + ", " + pincode.Taluk + ", " + pincode.Districtname + ", " + pincode.state + ", " + pincode.pincode
					results.append(pincode_json)
			else:
				cities = City.objects.filter(city__istartswith = q)
				for city in cities:
					city_json = {}
					city_json['id'] = city.id
					city_json['label'] = city.city
					city_json['value'] = city.city
					results.append(city_json)
				cities = City.objects.exclude(city = q).filter(city__icontains = q).order_by('city')
				airports = Airports.objects.filter(iata__istartswith = q) | Airports.objects.filter(name__icontains = q) | Airports.objects.filter(city__icontains = q)
				stations = RailwayStation.objects.filter(code__istartswith = q ) | RailwayStation.objects.filter(name__icontains = q )
				for city in cities:
					city_json = {}
					city_json['id'] = city.id
					city_json['label'] = city.city
					city_json['value'] = city.city
					results.append(city_json)
				results.append("")
				for airport in airports:
					airport_json = {}
					airport_json['id'] = airport.id
					airport_json['label'] = airport.name + ", " + airport.city + "  (" + airport.iata + ")" 
					airport_json['value'] = airport.name + ", " + airport.city + "  (" + airport.iata + ")" 
					results.append(airport_json)
				results.append("")
				for station in stations:
					station_json = {}
					station_json['id'] = station.id
					station_json['label'] = station.name + "  (" + station.code + ")"
					station_json['value'] = station.name + "  (" + station.code + ")"
					results.append(station_json)

			data = json.dumps(results)
		#except:
		#	pass
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)


# Method to receive latitude and longitude from browser and redirect to findClosestView
def browserView(request):
	if request.is_ajax():
		lat = request.POST.get('lati')
		longi = request.POST.get('longi')
		res_dict = findClosestView(lat, longi)
	else:
		res_dict = "Error"
	data = json.dumps(res_dict)
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)


# Method to receive location given bu user and redirect to findClosestView
def customInputView(request):
	if request.is_ajax():
		address = request.POST.get('addr')
		api_key = "AIzaSyDxbahKLpEfTXx45y519FKL58dTZ4-oSd8"
		api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
		api_response_dict = api_response.json()
		if api_response_dict['status'] == 'OK':
			latitude = api_response_dict['results'][0]['geometry']['location']['lat']
			longitude = api_response_dict['results'][0]['geometry']['location']['lng']
		else:
			latitude = 0
			longitude = 0

		res_dict = findClosestView(latitude, longitude)
	else:
		res_dict = "Error"
	data = json.dumps(res_dict)
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)



# Method for finding nearest railway station and airport
def findClosestView(lat, longi):
	airports = Airports.objects.all()
	minDist = 999999.00000
	nearestAirport = ""
	nearestStation = ""
	for airport in airports:
		dist = distance_bet_loc(lat, longi, airport.latitude, airport.longitude)
		if minDist > dist:
			minDist = dist
			nearestAirport = airport.name + ", " + airport.city + "  (" + airport.iata + ")"
	minDist = 999999.00000
	stations = RailwayStation.objects.all()
	for station in stations:
		dist = distance_bet_loc(lat, longi, station.latitude, station.longitude)
		if minDist > dist:
			minDist = dist
			nearestStation = station.name + "  (" + station.code + ")"
	minDist = 999999.00000
	cities = City.objects.all()
	for city in cities:
		dist = distance_bet_loc(lat, longi, city.latitude, city.longitude)
		if minDist > dist:
			minDist = dist
			nearestCity = city.city + ", " + city.state 
	res_dict = {}
	res_dict['airport'] = nearestAirport
	res_dict['station'] = nearestStation
	res_dict['city'] = nearestCity
	#return minDist
	return res_dict


def distance_bet_loc(lat1, lon1, lat2, lon2):
	# approximate radius of earth in km
	r = 6373.0
	# Convert latitude and longitude to 
    # spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
	phi1 = (90.0 - float(lat1)) * degrees_to_radians
	phi2 = (90.0 - float(lat2)) * degrees_to_radians
         
    # theta = longitude
	theta1 = float(lon1) * degrees_to_radians
	theta2 = float(lon2) * degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
	cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + 
           math.cos(phi1) * math.cos(phi2))
	arc = math.acos( cos )
	dist = r * arc
	return dist
	'''
	lat1 = float(lat1)
	lon1 = float(lon1)
	lat2 = float(lat2)
	lon2 = float(lon2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance
	'''



'''https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=YOUR_API_KEY'''

def test(request):	
	api_key = "AIzaSyAo8KHbyNizpXJuPTDXF0OwdOLQ38F_0-M"
	cities = City.objects.values_list('id', 'city', 'state').all()
	for city in cities:
		address = city[1] + ", " + city[2]
		api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
		api_response_dict = api_response.json()
		if api_response_dict['status'] == 'OK':
			latitude = api_response_dict['results'][0]['geometry']['location']['lat']
			longitude = api_response_dict['results'][0]['geometry']['location']['lng']
		else:
			latitude = 0
			longitude = 0
		ins = City.objects.get(id = city[0])
		ins.latitude = latitude
		ins.longitude = longitude
		ins.save()
	return render(request,'test.html',{"lat" : latitude, "long" : longitude})


'''	
	if request.method == "POST":
		cityName = request.POST['cityName']
		try:
			res = City.objects.values_list('city', flat = True).filter(city__icontains = cityName)
			data = serializers.serialize("json", res)
    		return HttpResponse(data, content_type ='application/json')
			return HttpResponse(res[0])
		except:
			return HttpResponse('Not Found...')
'''