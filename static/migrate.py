import sys
import cPickle as pickle
from sets import Set
from server import dynamic_trips
from server import routes

sys.modules['dynamic_trips'] = dynamic_trips
sys.modules['routes'] = routes

locs = Set([])
with open("server/.loc_file", 'r') as f:
	locs = pickle.load(f)

pickle.dump(locs, open(".loc_file", 'wb'))

trips = []
with open("server/.rides_def", 'r') as f:
	trips = pickle.load(f)

pickle.dump(trips, open(".rides_def", 'wb'))

cache = {}
with open("server/.routes_cache", 'r') as f:
	cache = pickle.load(f)

pickle.dump(cache, open(".routes_cache", 'wb'))
