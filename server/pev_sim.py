## TODO run simulation of a fleet of PEVs carrying out a
## a set of pickup/dropoff tasks

import fleet as pev

class Sim_env:
	def __init__(self, fleet_size, bounds, start_loc):
		self.bounds = bounds
		self.fleet = pev.Fleet(fleet_size, bounds, start_loc)

	 	## TODO support time chunks?
		self.sim_end = 0

		## time series data bucketed by 10 minutes
		self.util = []
		self.emissions = []
		self.wait_times = []

		self.trips = []

	def schedule(self, start_time, trips):
		## trips is a sorted list of Trip objects,
		## sorted by pickup time
		for t in trips:
			self.fleet.assign_task(t)
		self.fleet.finishUp()

		self.trips.extend(trips);
		self.util = self.fleet.getUtilization()
		self.emissions = self.fleet.getEmissions()

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

