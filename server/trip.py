## TODO a model for a request for pickup and delivery of a person or
## package

import routes
import sim_util

class Pickup:
	def __init__(self, uid, time, start, dest, is_human, route=None):
		self.uid = uid

		## convert to seconds after midnight
		self.time_ordered = sim_util.seconds_since_midnight(time)

		self.start_loc = start
		self.dest_loc = dest
		self.is_human = is_human
		self.pickup = 0
		if route is None:
			self.routefind()
		else:
			self.route = route
		## TODO: differing fare priority
		## TODO: arrival time for packages

	def approx_dur(self):
		## based on 10 mph, gives as-bird-flies in seconds
		return sim_util.ll_dist_m(self.start_loc, self.dest_loc) / 4.47 
		
	def routefind(self):
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
		else:
			return "PARCEL"

	def getRoute(self):
		return self.route

	def getDest(self):
		return self.dest_loc

	def getID(self):
		return self.uid

	def setPickup(self, wait):
		self.pickup = self.time_ordered + wait
