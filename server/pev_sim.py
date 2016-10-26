## TODO run simulation of a fleet of PEVs carrying out a
## a set of pickup/dropoff tasks

import fleet as pev
import os
import hashlib

class Sim_env:
	def __init__(self, fleet_size, bounds, starting_locs):
		self.bounds = bounds
		self.fleet_size = fleet_size
		self.starting_locs = starting_locs
		self.fleet = pev.Fleet(fleet_size, bounds, starting_locs)

		self.sim_start = 0
		self.sim_end = 0

		## time series data bucketed by 10 minutes
		self.util = []
		self.emissions = []
		self.wait_times = []
		self.ongoing = True

		self.trips = []
	
		self.sim_uid = str(hashlib.sha224(os.urandom(160)).hexdigest())

	def setFleetSize(self, size):
		self.fleet.setFleetSize(size)
		self.fleet_size = size
		

	def getSegment(self, start, end, ongoing):
		sgmnt = Sim_env(self.fleet_size, self.bounds, self.starting_locs)
		sgmnt.fleet = self.fleet.getSegment(start, end)
		sgmnt.sim_start = start
		sgmnt.sim_end = end
		sgmnt.sim_uid = self.sim_uid

		## sgmnt.util = self.fleet.getUtilization(start, end)
		sgmnt.util = self.fleet.getUtilization()

		## sgmnt.emissions = self.fleet.getEmissions(start, end)
		sgmnt.emissions = self.fleet.getEmissions()

		## filter trips by time ordered
		sgmnt.trips = []
		for trip in self.trips:
			if start <= trip.getTimeOrdered() and trip.getTimeOrdered() < end:
				sgmnt.trips.append(trip)
		sgmnt.ongoing = ongoing
		return sgmnt

	def scheduleIncremental(self, trips, dur):
		self.sim_start = self.sim_end
		for t in trips:
			self.fleet.assign_task(t)
		self.sim_end = self.sim_start + dur
		self.trips.extend(trips)

	def scheduleAll(self, trips):
		print "Assigning tasks..."
		## trips is a sorted list of Trip objects,
		## sorted by pickup time
		for t in trips:
			self.fleet.assign_task(t)
		print "Assigned!"
		self.fleet.finishUp() ## TODO don't "finish up" if we want to stream
		print "Closed simulation!"

		self.trips.extend(trips);

		print "extended data and logs!"

		## TODO update sim_end
		## TODO time series statistics

		## Fleet implementation:
		## for each vehicle, call the statistics method over the whole time range
		## Merge the results that each vehicle produces (mean of utilization, sum of emissions)

		## Vehicle implementation
		## given a time range:
		## create a set of 30-minute buckets
		## iterate over history
		## for each trip in history, apply to relevant buckets
		## utilization should be passengers or parcels * minutes of trip / bucket size
		## emissions should be total distance of any sort. For trips that span multiple buckets,
		## the distance should be prorated into each bucket

		## For getting wait times:
		## TODO: strategerize this one?

