import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta
from dateutil import tz
import random
from ast import literal_eval

def foo(fleetSize,chargingFleetSize):
    chargingData = pd.read_csv('dataprocessing/chargingData.csv')
    tripsData = pd.read_csv('dataprocessing/tripsData.csv')

    tripsData["pickupTime"] = pd.to_datetime(tripsData["pickupTime"])
    tripsData["dropoffTime"] = pd.to_datetime(tripsData["dropoffTime"])

    chargingData['startCharging_time'] = pd.to_datetime(chargingData['startCharging_time'])
    chargingData['endCharging_time'] = pd.to_datetime(chargingData['endCharging_time'])
    chargingData['start_time'] = pd.to_datetime(chargingData['start_time'])

    tripsData['pickupLocation'] = [literal_eval(x) for x in tripsData['pickupLocation']]
    tripsData['dropoffLocation'] = [literal_eval(x) for x in tripsData['dropoffLocation']]

    columns = ['trip_id', 'start_time', 'start_lon', 'start_lat', 'end_time',
               'end_lon', 'end_lat', 'charging', 'charging_time', 'charging_waittime']

    filtered_street = pd.DataFrame(columns = columns)

    random_trips = random.sample(range(0, len(tripsData)), fleetSize-chargingFleetSize)
    temp_len = len(filtered_street)
    for i,random_trip in enumerate(random_trips):
        print(i)
        temp_list = []
        temp_list.append(random_trip)
        temp_list.append(tripsData["pickupTime"][random_trip].strftime("%m/%d/%y %I:%M %p"))

        temp_list.append(tripsData["pickupLocation"][random_trip][0])
        temp_list.append(tripsData["pickupLocation"][random_trip][1])

        temp_list.append(tripsData["dropoffTime"][random_trip].strftime("%m/%d/%y %I:%M %p"))

        temp_list.append(tripsData["dropoffLocation"][random_trip][0])
        temp_list.append(tripsData["dropoffLocation"][random_trip][1])

        temp_list.append(0)
        temp_list.append(0)
        temp_list.append(0)
        filtered_street.loc[temp_len + i] = temp_list

    random_trips = random.sample(range(0, len(chargingData)), chargingFleetSize)
    temp_len = len(filtered_street)
    for i,random_trip in enumerate(random_trips):
        print(i)
        temp_list = []
        temp_list.append(random_trip)
        temp_list.append(chargingData['start_time'][random_trip].strftime("%m/%d/%y %I:%M %p"))
        temp_list.append(chargingData['startLocation_lon'][random_trip])
        temp_list.append(chargingData['startLocation_lat'][random_trip])
        temp_list.append((chargingData['startCharging_time'][random_trip] - timedelta(seconds=int(chargingData['waittime'][random_trip]))).strftime("%m/%d/%y %I:%M %p"))
        temp_list.append(chargingData['charging_longitude'][random_trip])
        temp_list.append(chargingData["charging_latitude"][random_trip])
        temp_list.append(1)
        temp_list.append(chargingData["ChargingDuration"][random_trip])
        temp_list.append(chargingData["waittime"][random_trip])
        filtered_street.loc[temp_len + i] = temp_list

    # filtered_street.to_csv('dataprocessing/run_sim.csv',index=False)
    filtered_street.to_csv('dataprocessing/run_sim.csv',index=False)



    return "created"
