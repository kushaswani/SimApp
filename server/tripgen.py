#TODO random trip generation
#TODO allow user to supply trip file
import csv
import trip
import sim_util

def readNewburyTestData():
	path = "../dataprocessing/filtered-street.csv"
	## TODO pop out into method
	trips = []
	with open(path, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			## Row format: (for this one file)
			## ID
			## Pickup time
			## Pickup address
			## Pickup latitude
			## Pickup Longitude	
			## Dropoff Time
			## Dropoff address
			## Dropoff Latitude
			## Dropoff Longitude
			try:
				start = (float(row[4]), float(row[3]))
				dest = (float(row[8]), float(row[7]))
				trips.append(trip.Pickup(
					int(row[0]),
					sim_util.timeify(row[1]),
					start, 
					dest,
					True) ## TODO packages?
				)
			except ValueError:
				pass
	## sort
	return sorted(trips, key=lambda task:task.getTimeOrdered())



