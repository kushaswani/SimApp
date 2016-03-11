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

def filterByStreet(zipped):
	filtered = {}
	for (id, datum) in zipped.items():
		if onStreet(datum):
			filtered[id] = datum
	return filtered

def onStreet(datum):
	pickup = datum["pickup"]
	dropoff = datum["dropoff"]
	return (pickup["addr"].find("Newbury") >= 0 or dropoff["addr"].find("Newbury") >= 0)

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

street = "Newbury"
pickups  = parseFiltered("./pickups.csv")
dropoffs = parseFiltered("./dropoffs.csv")
zipped = zipPickupDropoff(pickups, dropoffs)

filtered = filterByStreet(zipped)

csvdump("./filtered-street.csv", filtered)
