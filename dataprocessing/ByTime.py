import csv

def parseFiltered(path):
	parsed = {}
	with open(path, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			try:
				id = int(row[0])
				parsed[id] = {
					"date": row[1],
					"addr": row[2],
					"long" : float(row[3]),
					"lat" : float(row[4])
				}
			except ValueError:
				pass
	return parsed

def timeBucket(pickups, n):
	bucket = {}
	for (id, datum) in pickups.items():
		time = datum['date'].split(" ")
		hour = int(time[1].split(":")[0])

		if time[2] == "PM" and hour != 12:
			hour += 12
		elif time[2] == "AM" and hour == 12:
			hour -= 12

		if hour == n:
			bucket[id] = datum
	return bucket


def flatten((id, datum)):
	#python dictionary to row
	return ",".join([
		str(id),
		'"' + datum["date"] + '"',
		'"' + datum["addr"] + '"',
		str(datum["long"]),
		str(datum["lat"])
		])

def csvdump(path, bucket):
	#writes flattened lines to a csv file
	with open(path, "w") as out:
		for (id, datum) in bucket.items():
			out.write(flatten((id, datum)) + "\n")

pickups = parseFiltered("pevsummer-master/dataprocessing/filtered_pickups_9_12.csv")
for n in range(24):
	csvdump("/Users/yixingliu/Desktop/pevsummer-master/dataprocessing/ByTime/Hour_" + str(n) + ".csv", timeBucket(pickups, n))




