#TODO random trip generation
#TODO allow user to supply trip file

try:
	import trip
except:

	from server import trip
try:
	import sim_util
except:
	from server import sim_util

import csv

def readNewburyTestData(test,model_no):
	if test:
		path = "../dataprocessing/test_sim.csv"
	else:
		path = "dataprocessing/run_sim{}.csv".format(model_no)
	## TODO pop out into method
	trips = []
	print(path)
	with open(path, 'r') as file:
		reader = csv.reader(file)
		fields = reader.__next__()
		dict_ = {}
		# print(fields)
		for i,field in enumerate(fields):
			dict_[field] = i
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

				if int(row[dict_['charging']])==1:
					# print('test')
					is_human = False
					is_charging = True
				else:
					is_human = True
					is_charging = False
				# print(is_human)
				start = (float(row[dict_['start_lat']]), float(row[dict_['start_lon']]))
				dest = (float(row[dict_['end_lat']]), float(row[dict_['end_lon']]))
				charging_time = float(row[dict_['charging_time']])
				charging_waittime = float(row[dict_['charging_time']])

				ts = sim_util.timeify(row[dict_['start_time']])
				time_ordered = sim_util.seconds_since_midnight(ts)

				ts = sim_util.timeify(row[dict_['end_time']])
				trip_time = sim_util.seconds_since_midnight(ts) - time_ordered

				trips.append(trip.Pickup(
					int(row[dict_['trip_id']]),
					time_ordered,
					trip_time,
					start,
					dest,
					is_human,
					is_charging,
					charging_time,
					charging_waittime) ## TODO packages?
				)
			except ValueError:
				pass
	## sort
	return sorted(trips, key=lambda task:task.getTimeOrdered())
