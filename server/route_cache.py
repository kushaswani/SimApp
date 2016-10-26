from pymongo import MongoClient, GEO2D

class RouteCache:
	
	def __init__(self, dbname):
		self.client = MongoClient()
		self.db = self.client[dbname]
		self.places = self.db.places

	def hasRoute(self, ori, dst):
		return (not (self.places.find_one({"ends": [ori,dst]}) is None))

	def getRoute(self, ori, dst):
		found = self.places.find_one({"ends": [ori, dst]})
		return found["route"]

	def setRoute(self, ori, dst, rte):
		self.places.insert({"ends":[ori, dst], "route": rte})

	def save(self):
		pass

	def close(self):
		pass
