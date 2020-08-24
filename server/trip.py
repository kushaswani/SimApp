## TODO a model for a request for pickup and delivery of a person or
## package



try:
	import routes
except:
	from server import routes

try:
	import sim_util
except:
	from server import sim_util

import re

class Pickup:
	def __init__(self, uid, time_ordered, trip_time, start, dest, is_human, is_charging, charging_time, charging_waittime, route=None):
		self.uid = uid

		## convert to seconds after midnight
		# print(time)

		# try:
		# 	self.time_ordered = sim_util.seconds_since_midnight(time)
		# except:
		# 	self.time_ordered = time

		self.time_ordered = time_ordered

		self.trip_time = trip_time
		# print(self.time_ordered)
		self.start_loc = start
		self.dest_loc = dest
		self.is_human = bool(is_human)
		self.is_charging = bool(is_charging)
		self.pickup = 0
		self.charging_time = charging_time
		self.charging_waittime = charging_waittime
		if route is None:
			self.routefind()
		else:
			self.route = route

		if trip_time is None:
			temp = list(map(int, re.findall(r'\d+', self.route.rte['legs'][0]['duration']['text']) ))
			self.trip_time = temp[0]*60
		else:
			self.route.duration = trip_time
		## TODO: differing fare priority
		## TODO: arrival time for packages

	def approx_dur(self):
		## based on 10 mph, gives as-bird-flies in seconds
		return sim_util.ll_dist_m(self.start_loc, self.dest_loc) / 4.47

	def routefind(self):
		# print(self.start_loc)
		# print(self.dest_loc)
		# print(routes.RouteFinder().client)
		self.route = routes.RouteFinder().get_dirs(self.start_loc, self.dest_loc)
		if self.route is None:
			raise Exception("could not find route")
		# self.duration = self.route.getDuration()

	def getTimeOrdered(self):
		return self.time_ordered

	def getPickupLoc(self):
		return self.start_loc

	def getDuration(self):
		return self.route.getDuration()

	def getType(self):
		if self.is_human:
			return "PASSENGER"
		elif self.is_charging:
			return "CHARGING"
		else:
			return "NAV"

	def getRoute(self):
		return self.route

	def getDest(self):
		return self.dest_loc

	def getID(self):
		return self.uid

	def setPickup(self, wait):
		self.pickup = self.time_ordered + wait
