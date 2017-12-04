import json
import urllib.request

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
