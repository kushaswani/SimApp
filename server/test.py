#!/usr/bin/env python
## TODO a test case

import tripgen
import pev_sim
import pprint
import sim_util
import routes

import json

routes.RouteFinder("google_api_key", ".routes_cache")

env = pev_sim.Sim_env(3, None, (42.3492699,-71.0900377))

testdata = tripgen.readNewburyTestData()

for t in testdata:
	print " ".join(["Trip", str(t.getID()), "Time", str(t.getTimeOrdered()), "Pickup:", str(t.getPickupLoc()), "Dropoff", str(t.getDest())])

env.schedule(None, testdata)

pp = pprint.PrettyPrinter(indent=4)
## pp.pprint(env.fleet.vehicles)
print json.dumps(env, default=sim_util.default_json, separators=(',', ':'), indent=4)
