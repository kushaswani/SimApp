## TODO utility functions for the simulation
from geopy.distance import great_circle
from time import strptime
from collections import deque
import datetime

def center_of(bounds):
	raise(NotImplementedError)

def ll_dist_m(a, b):
	return great_circle(a, b).meters

def timeify(s):
	return strptime(s, "%m/%d/%y %I:%M %p") 

def seconds_since_midnight(ts):
	if type(ts) is int:
		return ts
	td = datetime.timedelta(hours=ts.tm_hour, minutes=ts.tm_min)
	return td.seconds

def default_json(o):
	return o.__dict__

