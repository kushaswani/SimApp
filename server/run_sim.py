import dynamic_trips
import pev_sim
import sim_util
import json

def Run(fleet, maxDist, freq, start, end):
	pickups = dynamic_trips.TripRandomizer().assembleTripSim(maxDist, freq, maxDist, freq, start, end)
	env = pev_sim.Sim_env(fleet, None, (42.3602595, -71.0873766))
	env.schedule(None, pickups)
	return json.dumps(env, default=sim_util.default_json, separators=(',', ':'), indent=4)

#from chew

# import dynamic_trips
# import pev_sim
# import sim_util
# import json

# environs = {}


# def Run(sim_uid, fleet, maxDist, freq, dur):
# 	start = 0
# 	if sim_uid in environs:
# 		env = environs[sim_uid]
# 		start = env.sim_end
# 		env.setFleetSize(fleet)
# 	else:
# 		global hubway_stations
# 		env = pev_sim.Sim_env(fleet, None, hubway_stations)
# 	end = start + dur
# 	pickups = dynamic_trips.TripRandomizer().assembleTripSim(maxDist, freq, maxDist, freq, start, end)
# 	env.scheduleIncremental(pickups, dur)
# 	environs[env.sim_uid] = env
# 	return json.dumps(env.getSegment(start, end, True), default=sim_util.default_json, separators=(',', ':'), indent=4)
