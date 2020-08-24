#!/usr/bin/env python
## TODO the server that runs the simulation. Should receive
## requests from the front end, dispatch the simulation,
## and update the front end with visualization data

## server code courtesy of https://snipt.net/raw/f8ef141069c3e7ac7e0134c6b58c25bf/?nice
## @rochacbruno

import SimpleHTTPServer
import SocketServer
import logging
import json
import server

import sys


PORT = 8233


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
	logging.warning(" PATH: " + self.path)
        logging.warning(self.headers)
        logging.warning("======= POST VALUES =======")

	length = int(self.headers['Content-Length'])
	data = self.rfile.read(length)
	logging.warning("Received: " + data)
        logging.warning("\n")
	if self.path == "/fleetsim":
		## do fleet sim stuff
		args = json.loads(data)
		fleet_size = int(args["size"])
		(dist, units) = args["maxDist"].split()
		maxDist = int(dist) * 1600
		parcFreq = int(args["parcels"].split()[0])
		print fleet_size
		print maxDist
		print parcFreq
		response = server.run_sim.Run(fleet_size, maxDist, parcFreq, 0, 28800)
		self.wfile.write(response)
	else:
        	SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

# initialize simulation stuff
server.routes.RouteFinder("google_api_key", ".routes_cache")
server.dynamic_trips.TripRandomizer().loadLocsFile(".loc_file")
server.dynamic_trips.TripRandomizer().loadRidesFile(".rides_def")
Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

httpd.serve_forever()
