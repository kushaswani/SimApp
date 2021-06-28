import flask
import pickle
import pandas as pd
import csv
import io
import os
import numpy as np
from flask import Flask, flash, request, redirect, url_for, jsonify
import sys

from werkzeug.utils import secure_filename

from server import run_sim

from dataprocessing import get_run_sim_data

from datetime import timedelta
from ast import literal_eval







UPLOAD_FOLDER = '/home/xyz/Documents/webapp/uploads'
# Initialise the Flask app
app = flask.Flask(__name__, template_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up the main route
@app.route('/', methods=['GET'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('map.html'))


@app.route('/run/', methods=['POST'])
def run():
    # try:
    if flask.request.method == 'POST':
        # msg = request.get_data()
        # msg = msg.decode("utf-8")
        # msg = literal_eval(msg)

        msg = request.get_json()

        # print(msg)
        fleetSize = int(msg['size'])
        chargingFleetSize = int(msg['chargingSize'])
        get_run_sim_data.foo(fleetSize,chargingFleetSize,1)
        get_run_sim_data.foo(fleetSize,chargingFleetSize,2)
        # temp_data = run_sim.save_run_sim_json(20,6)
        run_sim.save_run_sim_json(fleetSize,chargingFleetSize)
        # except:
        #     print("error")
        data = {'file_path1': 'static/json_files/run_sim1.json','file_path2': 'static/json_files/run_sim2.json'}
        data = jsonify(data)
        return data

if __name__ == '__main__':
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    app.run(debug = True)
