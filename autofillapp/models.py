from django.db import models

class City(models.Model):

	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 50)
	population = models.IntegerField()
	latitude = models.CharField(max_length = 20)
	longitude = models.CharField(max_length = 20)
	class Meta:
#		db_table = "indianCities"
		db_table = "city"


class Airports(models.Model):

	icao = models.CharField(max_length = 5)
	name = models.CharField(max_length = 50)
	latitude = models.CharField(max_length = 50)
	longitude = models.CharField(max_length = 50)
	city = models.CharField(max_length = 25)
	iata = models.CharField(max_length = 6)
	class Meta:
		db_table = "indian_Airports"


class RailwayStation(models.Model):

	name = models.CharField(max_length = 40)
	code = models.CharField(max_length = 5)
	state = models.CharField(max_length = 2)
	zone = models.CharField(max_length = 4)
	latitude = models.CharField(max_length = 20)
	longitude = models.CharField(max_length = 20)
	class Meta:
		db_table = "railwayStation"


class Pincode(models.Model):

	officeName = models.CharField(max_length = 50)
	pincode = models.CharField(max_length = 7)
	Taluk = models.CharField(max_length = 35)
	Districtname = models.CharField(max_length = 20)
	divisionname = models.CharField(max_length = 25)
	regionname = models.CharField(max_length = 20)
	state = models.CharField(max_length = 20)
	class Meta:
		db_table = "pincode"