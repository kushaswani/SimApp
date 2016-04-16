## TODO an algorithm for assigning a task to a fleet
## Should run on-line (that is, without knowledge of
## upcoming tasks)
import fleet
from sets import Set

def assign(time, task, fleet):
	## strawman - assign task to soonest free member
	illegal = Set([])
	while len(illegal) < len(fleet.vehicles):
		assignee = None
		for pev in fleet:
			if not pev.getUID() in illegal:
				if assignee is None:
					assignee = pev
				elif pev.soonestFreeAfter(time) < assignee.soonestFreeAfter(time):
					assignee = pev
		try: 
			wait_time = assignee.assign(task, time)
			task.setPickup(wait_time)
			return (assignee.getUID(), wait_time)
		except:
			illegal.add(assignee.getUID())
	raise Exception("Simulation died - no vehicles could accept task " + str(task))
