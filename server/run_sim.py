#!/usr/bin/env python
## TODO a test case

try:
	from server import tripgen
	from server import pev_sim
	from server import sim_util
	from server import routes
except:
	import tripgen
	import pev_sim
	import sim_util
	import routes

import json
import pprint

def save_run_sim_json(fleetSize, chargingFleetSize):
	routes.RouteFinder("server/google_api_key", ".routes_cache")
	#print("test",flush = True)
	# env = pev_sim.Sim_env(3, None, (42.3492699,-71.0900377))
	env = pev_sim.Sim_env(fleetSize - chargingFleetSize, None, (22.534901,114.007896))

	testdata = tripgen.readNewburyTestData(test = False)

	for t in testdata:
		print(" ".join(["Trip", str(t.getID()), "Time", str(t.getTimeOrdered()), "Pickup:", str(t.getPickupLoc()), "Dropoff", str(t.getDest())]))

	env.schedule(None, testdata)

	pp = pprint.PrettyPrinter(indent=4)
	## pp.pprint(env.fleet.vehicles)
	json_content = json.dumps(env, default=sim_util.default_json, separators=(',', ':'), indent=4)


	# print json.dumps(env, default=sim_util.default_json, separators=(',', ':'), indent=4)
	with open('static/json_files/run_sim.json', 'w') as f:
	    f.write(json_content)
