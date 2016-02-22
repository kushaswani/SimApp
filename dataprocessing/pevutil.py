import csv
import datetime

"""
Useful, reusable functions.
"""

def toDateTime(point, datum):
    # point can be "pickup" or "dropoff"
    time = datum[point]["date"].split(" ")

    month   = int(time[0].split("/")[0])
    day     = int(time[0].split("/")[1])
    year    = int(time[0].split("/")[2])

    hour    = int(time[1].split(":")[0])
    minute  = int(time[1].split(":")[1])

    if time[2] =='PM' and hour!=12:
        hour += 12
    elif time[2] =='AM' and hour==12:
        hour-=12
        
    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

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
    for key in pickups.keys():
        try:
            zipped[key] = {
                "pickup": pickups[key].copy(),
                "dropoff": dropoffs[key].copy()
            }
        except KeyError:
            pass
    return zipped

def flatten(id, datum):
    pickup  = datum["pickup"]
    dropoff = datum["dropoff"]
    return ",".join([
        str(id),
        '"' + pickup["date"] + '"',
        '"' + pickup["addr"] + '"',
        str(pickup["lat"]),
        str(pickup["long"]),
        '"' + dropoff["date"] + '"',
        '"' + dropoff["addr"] + '"',
        str(dropoff["lat"]),
        str(dropoff["long"])])

def csvdump(path, zipped):
    with open(path, "w") as out:
        for (id, datum) in zipped.items():
            out.write(flatten(id, datum) + "\n")
