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

				if int(row[9])==1:
					# print('test')
					is_human = False
				else:
					is_human = True
				# print(is_human)
				start = (float(row[4]), float(row[3]))
				dest = (float(row[8]), float(row[7]))
				charging_time = float(row[10])
				charging_waittime = float(row[11])

				ts = sim_util.timeify(row[1])
				time_ordered = sim_util.seconds_since_midnight(ts)

				ts = sim_util.timeify(row[5])
				trip_time = sim_util.seconds_since_midnight(ts) - time_ordered

				trips.append(trip.Pickup(
					int(row[0]),
					time_ordered,
					trip_time,
					start,
					dest,
					is_human,
					charging_time,
					charging_waittime) ## TODO packages?
				)
			except ValueError:
				pass
	## sort
	return sorted(trips, key=lambda task:task.getTimeOrdered())
