"""
find_store

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>             Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>     Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=<(mi|km)>         Display units in miles or kilometers [default: mi]
  --output=<(text|json)>    Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
"""

import csv
import json
import os
import sys
from retrying import retry
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
sys.path.append(os.path.join(os.path.dirname(__file__)))

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

result_template = """
Address:
{}
{}
Distance: {} {}
"""

print(sys.argv)

@retry(stop_max_attempt_number=7, wait_fixed=500)
def get_lat_lng(address):
  try:
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    lat_lng = (location.latitude, location.longitude)
  finally:
    return lat_lng

def find_closest_lat_lng(user_lat_lng, coords):
  """ Find closest lat lng coord from list of coords """
  closest = {
    "coord": None,
    "distance_data": None,
  }
  # TODO - Restructure coords to reduce calculation time
  for coord in coords:
    distance_data = geodesic(user_lat_lng, coord['lat_lng'])
    if not closest["coord"] or distance_data.miles < closest["distance_data"].miles:
      closest["distance_data"] = distance_data
      closest["coord"] = coord
  return closest

def provide_output(data, units, output):
  """ Output data """
  record = data["coord"]["record"]
  address1 = record[2]
  address2 = str.join(", ", (record[3], record[4])) + " " + record[5]
  output_data = {
    "distance": data["distance_data"].__getattribute__(units),
    "units": units,
    "data": data["coord"]["record"],
    "address": [address1, address2]
  }
  output_text = ''
  
  if output == 'json':
    output_text = json.dumps(output_data, indent=4, sort_keys=True)
  else:
    output_text = result_template.format(address1, address2, output_data["distance"], units)
    
  print(output_text)
  return output_data, output_text

def main():
    """ Main CLI entrypoint. """
    options = docopt(__doc__, version=VERSION)

    result = {}
    
    address = options.get('--address')
    zipcode = options.get('--zip')
    units = options.get('--units')
    output = options.get('--output')
    
    challenge_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "code-challenge/store-locations.csv")
    
    with open(challenge_dir) as store_locations_csv_file:
      reader = csv.reader(store_locations_csv_file)
      store_locations = list(reader)
      store_locations.pop(0)
      lat_lngs = [{ 'lat_lng': (record[6], record[7]), 'record': record } for record in store_locations]
      user_lat_lng = get_lat_lng(address or zipcode)
      closest = find_closest_lat_lng(user_lat_lng, lat_lngs)
      result = provide_output(closest, units, output)
    
    return result

if __name__ == '__main__':
  main()
