from server import *

dynamic_trips.TripRandomizer().loadLocsFile(".loc_file")
for i in xrange(24):
	dynamic_trips.TripRandomizer().loadCSVLocs("dataprocessing/bucketsamples/Hour_" + str(i) + "_100.csv")
