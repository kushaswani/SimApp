from server import *

dynamic_trips.TripRandomizer()
dynamic_trips.TripRandomizer().loadLocsFile(".loc_file")
dynamic_trips.TripRandomizer().loadRidesFile(".rides_def")

routes.RouteFinder("server/google_api_key", ".routes_cache")

print run_sim.Run(15, 4800, 3, 0, 28800)
