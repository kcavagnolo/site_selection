import pandas as pd
import sys
from numpy import sin, cos, pi, arcsin, sqrt, arctan2
from pygeocoder import Geocoder

api_key = "AIzaSyC71IyZZ5uATPaJmwhZpelBJqMI76ui6Ag"

def get_dist(lat, lon, lat0, lon0):
  radf = pi / 180.0
  rlat = lat * radf
  rlon = lon * radf
  rlat0 = lat0 * radf
  rlon0 = lon0 * radf
  delta_lon = rlon - rlon0
  delta_lat = rlat - rlat0
  n1 = cos(rlat)*sin(delta_lon)
  n2 = (cos(rlat0)*sin(rlat))-(sin(rlat0)*cos(rlat)*cos(delta_lon))
  d1 = sin(rlat0)*sin(rlat)
  d2 = cos(rlat0)*cos(rlat)*cos(delta_lon)
  ay = sqrt(n1**2+n2**2)
  ax = (d1+d2)
  vangle = arctan2(ay,ax)
  erad = 6371  # kilometers
  return (vangle * erad)

# read dataframe
f = open(sys.argv[0], 'rb')
df = pd.read_csv(sys.argv[1])

# iteration start point
lat0 = float(sys.argv[2])
lon0 = float(sys.argv[3])
nit = int(sys.argv[4])

# optimization iterations
costs = []
for i in range(0,nit):
  dist = get_dist(df.lat, df.lon, lat0, lon0)
  denom = df.demand/dist
  numx = df.demand*df.lat/dist
  numy = df.demand*df.lon/dist
  lat0 = sum(numx)/sum(denom)
  lon0 = sum(numy)/sum(denom)
  costs.append(sum(df.demand*dist))
  if 1.0-(costs[i]/costs[i-1]) < 1e-6 and i != 0:
    break
#  print "Optimal site\nlat: %f, lon: %f" % (lat0, lon0)
  print "New Address: %s" % Geocoder.reverse_geocode(lat0,lon0)[0]

print "Optimal site\nlat: %f, lon: %f" % (lat0, lon0)
print "Address: %s" % Geocoder.reverse_geocode(lat0,lon0)[0]
