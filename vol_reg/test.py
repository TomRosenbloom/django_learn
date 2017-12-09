from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from everystreet.models import *

place = Point(-2.929060, 54.896065, srid=4326)
radius = D(mi=10)

postcodes = Postcode.objects.annotate(
	distance=Distance('location',place)
).filter(
	location__distance_lte=(place,radius)
).order_by('distance')

for postcode in postcodes:
	print(postcode.distance.mi)
