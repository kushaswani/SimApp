import random
import time
import cPickle as pickle
import routes
import csv
from sets import Set

import sim_util
import trip

class TripRandomizer:
	class __Singleton:
		def __init__(self):
			self.locs = Set([])
			self.locs_file = None
			self.trips = []
			self.rides_file = None

	instance = None
	def __init__(self):
		if TripRandomizer.instance:
			return
		else:
			TripRandomizer.instance = TripRandomizer.__Singleton()

	def saveLocsFile(self):
		if TripRandomizer.instance.locs_file:
			pickle.dump(TripRandomizer.instance.locs, open(TripRandomizer.instance.locs_file, 'wb'))

	def loadLocsFile(self, locs_file):
		self.saveLocsFile()
		TripRandomizer.instance.locs_file = locs_file
		try:
			with open(TripRandomizer.instance.locs_file, 'r') as f:
				TripRandomizer.instance.locs = pickle.load(f)
		except IOError:
			print "Could not open file " + locs_file
		except Exception as e:
			raise(e)

	def loadRidesFile(self, rides_file):
		self.saveRidesFile()
		TripRandomizer.instance.rides_file = rides_file
		try:
			with open(TripRandomizer.instance.rides_file, 'r') as f:
				TripRandomizer.instance.trips = pickle.load(f)
		except IOError:
			print "Could not open file " + rides_file
		except Exception as e:
			raise(e)

	def saveRidesFile(self):
		if TripRandomizer.instance.rides_file:
			pickle.dump(TripRandomizer.instance.trips, open(TripRandomizer.instance.rides_file, 'wb'))

	def loadCSVLocs(self, loc_csv):
		with open(loc_csv, 'r') as c:
			reader = csv.reader(c)
			for row in reader:
				try:
					TripRandomizer.instance.locs.add((float(row[4]), float(row[3])))
					TripRandomizer.instance.locs.add((float(row[8]), float(row[7])))
				except ValueError:
					pass
		self.saveLocsFile()

	def getTripLocation(self, maxDist):
		random.seed()
		if maxDist is None or maxDist <= 0:
			return random.sample(TripRandomizer.instance.locs, 2)
		scaleFactor = 4
		pulledPoints = random.sample(TripRandomizer.instance.locs, scaleFactor)
	
		## low-overhead O(n^2) algorithm with some
		## intelligence to reduce duplicated work
		## Probably somewhat fast for large maxDist
		checked = 0
		while True:
			## invariant: no pairs (pp[i], pp[j]) for i, j < checked qualify (are nearer than maxDist)
			for i in xrange(checked, len(pulledPoints)):
				for j in xrange(len(pulledPoints)):
					if i != j and sim_util.ll_dist_m(pulledPoints[i], pulledPoints[j]) <= maxDist:
						return (pulledPoints[i], pulledPoints[j])
			checked = len(pulledPoints)
			pulledPoints.extend(random.sample(TripRandomizer.instance.locs, scaleFactor))

	def randomizedPreprocessedRides(self, frequency, maxDist, start, end):
		print "Generating from " + str(len(TripRandomizer.instance. trips)) + " source trips"
		tripTimes = getRandomTripTimes(frequency, start, end)
		print "generating trips for " + str(len(tripTimes)) + " times"

		if len(TripRandomizer.instance.trips) < len(tripTimes):
			## if we don't have enough trips, randomly generate a few more
			self.genRides(maxDist + maxDist / 2, len(tripTimes))

	        idx = 0
		for t in TripRandomizer.instance.trips:
			idx += 1
			if t.dist > float(maxDist):
				break
		print "found " + str(idx - 1) + " trips shorter than " + str(maxDist)
		random.seed()
		if idx - 1 < len(tripTimes):
			rides = [random.sample(TripRandomizer.instance.trips[:idx], 1) for i in xrange(len(tripTimes))]
			return zip(tripTimes, rides)
		else:
			return zip(tripTimes, random.sample(TripRandomizer.instance.trips[:idx], len(tripTimes)))

	def assembleTripSim(self, hMaxDist, hFreq, pMaxDist, pFreq, start, end):
		humanRiders = self.randomizedPreprocessedRides(hFreq, hMaxDist, start, end)
		parcels = self.randomizedPreprocessedRides(pFreq, pMaxDist, start, end)
		pickups = []
		ids = 0
		for h in humanRiders:
			pickups.append(trip.Pickup(ids, h[0], h[1].start, h[1].dest, True, route=h[1].route))
			ids += 1
		for p in parcels:
			pickups.append(trip.Pickup(ids, p[0], p[1].start, p[1].dest, False, route=p[1].route))
			ids += 1
		pickups.sort(key=lambda x: x.getTimeOrdered())
		return pickups

	def genRides(self, maxDist, total):
		f = routes.RouteFinder()
		tn = total / (maxDist / 800)
		
		for rideDist in xrange(0, maxDist, 800):
			for i in xrange(tn):
				(start, dest) = self.getTripLocation(rideDist)
				rte = f.get_dirs(start, dest)
				if rte is not None:
					TripRandomizer.instance.trips.append(Ride(start, dest, sim_util.ll_dist_m(start, dest), rte))
		
		TripRandomizer.instance.trips.sort(key=lambda x: x.dist)
		
		self.saveRidesFile()


class Ride:
	def __init__(self, start, dest, dist, route):
		self.start = start
		self.dest = dest
		self.dist = dist
		self.route = route
	def __repr__(self):
		return repr((self.dist, self.start, self.dest))



def getRandomTripTimes(frequency, start, end):
	random.seed()
	mu = frequency * float(end - start) / 3600
	num_trips = int(random.gauss(mu, mu / 10))
	out = []
	for i in xrange(num_trips):
		out.append(random.randint(start, end))
	out.sort()
	return out


	


