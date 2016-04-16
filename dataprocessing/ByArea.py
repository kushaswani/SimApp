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


def zipPickupDropoff(pickups, dropoffs):
	zipped = {}
	for id in pickups.keys():
		try:
			zipped[id] = {
				"pickup": pickups[id].copy(),
				"dropoff": dropoffs[id].copy()
			}
		except KeyError:
			pass
	return zipped

def inArea(point, minCoord, maxCoord):
	print "point is " + str(point)
	return point[0] > minCoord[0] and point[1] > minCoord[1] and point[0] < maxCoord[0] and point[1] < maxCoord[1]

def filterByArea(zipped, minCoord, maxCoord):
	filtered = {}
	for (id, datum) in zipped.items():
		dropoff = datum["dropoff"]
		pickup = datum["pickup"]
		dropoffPoint = (dropoff["lat"], dropoff["long"])
		pickupPoint = (pickup["lat"], pickup["long"])
		print dropoffPoint
		print pickupPoint
		if inArea(pickupPoint, minCoord, maxCoord) and inArea(dropoffPoint, minCoord, maxCoord):
			filtered[id] = datum
	return filtered

def flatten(id, datum):
	#python dictionary to row
	pickup = datum["pickup"]
	dropoff = datum["dropoff"]

	return ",".join([
		str(id),
		'"' + pickup["date"] + '"',
		'"' + pickup["addr"] + '"',
		str(pickup["long"]),
		str(pickup["lat"]),
		'"' + dropoff["date"] + '"',
        '"' + dropoff["addr"] + '"',
        str(dropoff["long"]),
        str(dropoff["lat"])
        ])

def csvdump(path, zipped):
	#writes flattened lines to a csv file
	with open(path, "w") as out:
		for (id, datum) in zipped.items():
			out.write(flatten(id, datum) + "\n")

minCoord = (42, -71.02)
maxCoord = (43, -71)
pickups  = parseFiltered("/Users/yixingliu/Desktop/pevsummer-master/dataprocessing/filtered_pickups_9_12.csv")
dropoffs = parseFiltered("/Users/yixingliu/Desktop/pevsummer-master/dataprocessing/filtered_dropoffs_9_12.csv")
zipped = zipPickupDropoff(pickups, dropoffs)
#csvdump("/Users/yixingliu/Desktop/pevsummer-master/dataprocessing/filtered-all.csv", zipped)
filtered = filterByArea(zipped, minCoord, maxCoord)
csvdump("/Users/yixingliu/Desktop/pevsummer-master/dataprocessing/filtered-some.csv", filtered)
for id in filtered.keys():
	print id
print "Number: " + str(len(filtered))
