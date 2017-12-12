import json
import urllib.request
from math import radians, degrees, acos, sin, cos

def distance(lat1, lng1, lat2, lng2):
    # https://www.mullie.eu/geographic-searches/

    # convert latitude/longitude degrees for both coordinates
    # to radians: radian = degree * π / 180
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    # calculate great-circle distance
    distance = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lng1 - lng2))

    # distance in human-readable format:
    # earth's radius in km = ~6371
    return 6371 * distance


def square_around_origin(distance, origin_lat, origin_long):
    radius = 6371
    north_lat = origin_lat + degrees(distance/radius)
    south_lat = origin_lat - degrees(distance/radius)
    east_long = origin_long + degrees(distance/radius/cos(radians(origin_lat)))
    west_long = origin_long - degrees(distance/radius/cos(radians(origin_lat)))
    return ('Square',[north_lat, south_lat, east_long, west_long]) #named tuple

def postcodes_in_square(square):
    bounds = square[1]
    north_lat = bounds[0]
    south_lat = bounds[1]
    east_long = bounds[2]
    west_long = bounds[3]
    from backend.models import Postcode
    return(Postcode.objects.filter(latitude__gte=south_lat, latitude__lte=north_lat, longitude__gte=west_long, longitude__lte=east_long))

def postcodes_in_circle(postcodes_in_square, origin_lat, origin_long, radius):
    postcodes = []
    for postcode in postcodes_in_square:
        if distance(postcode.latitude, postcode.longitude, origin_lat, origin_long) <= radius:
            postcodes.append(postcode)
    return (postcodes)

def postcode_lookup(postcode):
    """
    Given a (valid) postcode, return details from postcodes.io
    use json.loads to convert the json response to python dictionary before returning
    Example response:
        {
        "status": 200,
        "result": {
            "postcode": "EX4 2LG",
            "quality": 1,
            "eastings": 287040,
            "northings": 94623,
            "country": "England",
            "nhs_ha": "South West",
            "longitude": -3.60225065630703,
            "latitude": 50.740201781113,
            "european_electoral_region": "South West",
            "primary_care_trust": "Devon",
            "region": "South West",
            "lsoa": "Teignbridge 001B",
            "msoa": "Teignbridge 001",
            "incode": "2LG",
            "outcode": "EX4",
            "parliamentary_constituency": "Central Devon",
            "admin_district": "Teignbridge",
            "parish": "Whitestone",
            "admin_county": "Devon",
            "admin_ward": "Teignbridge North",
            "ccg": "NHS Northern, Eastern and Western Devon",
            "nuts": "Devon CC",
            "codes": {
                "admin_district": "E07000045",
                "admin_county": "E10000008",
                "admin_ward": "E05003610",
                "parish": "E04003237",
                "parliamentary_constituency": "E14000623",
                "ccg": "E38000129",
                "nuts": "UKK43"
            }
        }
    }

    Example usage:
        print(postcode_lookup('ex42lg')['result']['longitude'])
    """
    postcode_lookup_url = 'http://api.postcodes.io/postcodes/'+postcode
    response = urllib.request.urlopen(postcode_lookup_url)
    return json.loads(response.read())


def postcodes_in_radius(radius, lat, long):
    postcodes = []
    postcodes_square = postcodes_in_square(square_around_origin(radius,lat,long))
    #print(postcodes_square)
    for postcode in postcodes_in_circle(postcodes_square, lat, long, radius):
        postcodes.append(postcode)
        #print(postcode.postcode)
        # why do the postcodes not have spaces?
    return postcodes
