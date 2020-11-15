import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta
from dateutil import tz
import random
from ast import literal_eval
import googlemaps
from datetime import datetime
import csv

# def foo(fleetSize,chargingFleetSize):
#     chargingData = pd.read_csv('dataprocessing/chargingData.csv')
#     tripsData = pd.read_csv('dataprocessing/tripsData.csv')
#
#     tripsData["pickupTime"] = pd.to_datetime(tripsData["pickupTime"])
#     tripsData["dropoffTime"] = pd.to_datetime(tripsData["dropoffTime"])
#
#     chargingData['startCharging_time'] = pd.to_datetime(chargingData['startCharging_time'])
#     chargingData['endCharging_time'] = pd.to_datetime(chargingData['endCharging_time'])
#     chargingData['start_time'] = pd.to_datetime(chargingData['start_time'])
#
#     tripsData['pickupLocation'] = [literal_eval(x) for x in tripsData['pickupLocation']]
#     tripsData['dropoffLocation'] = [literal_eval(x) for x in tripsData['dropoffLocation']]
#
#     columns = ['trip_id', 'start_time', 'start_lon', 'start_lat', 'end_time',
#                'end_lon', 'end_lat', 'charging', 'charging_time', 'charging_waittime']
#
#     filtered_street = pd.DataFrame(columns = columns)
#
#     random_trips = random.sample(range(0, len(tripsData)), fleetSize-chargingFleetSize)
#     temp_len = len(filtered_street)
#     for i,random_trip in enumerate(random_trips):
#         print(i)
#         temp_list = []
#         temp_list.append(random_trip)
#         temp_list.append(tripsData["pickupTime"][random_trip].strftime("%m/%d/%y %I:%M %p"))
#
#         temp_list.append(tripsData["pickupLocation"][random_trip][0])
#         temp_list.append(tripsData["pickupLocation"][random_trip][1])
#
#         temp_list.append(tripsData["dropoffTime"][random_trip].strftime("%m/%d/%y %I:%M %p"))
#
#         temp_list.append(tripsData["dropoffLocation"][random_trip][0])
#         temp_list.append(tripsData["dropoffLocation"][random_trip][1])
#
#         temp_list.append(0)
#         temp_list.append(0)
#         temp_list.append(0)
#         filtered_street.loc[temp_len + i] = temp_list
#
#     random_trips = random.sample(range(0, len(chargingData)), chargingFleetSize)
#     temp_len = len(filtered_street)
#     for i,random_trip in enumerate(random_trips):
#         print(i)
#         temp_list = []
#         temp_list.append(random_trip)
#         temp_list.append(chargingData['start_time'][random_trip].strftime("%m/%d/%y %I:%M %p"))
#         temp_list.append(chargingData['startLocation_lon'][random_trip])
#         temp_list.append(chargingData['startLocation_lat'][random_trip])
#         temp_list.append((chargingData['startCharging_time'][random_trip] - timedelta(seconds=int(chargingData['waittime'][random_trip]))).strftime("%m/%d/%y %I:%M %p"))
#         temp_list.append(chargingData['charging_longitude'][random_trip])
#         temp_list.append(chargingData["charging_latitude"][random_trip])
#         temp_list.append(1)
#         temp_list.append(chargingData["ChargingDuration"][random_trip])
#         temp_list.append(chargingData["waittime"][random_trip])
#         filtered_street.loc[temp_len + i] = temp_list
#
#     # filtered_street.to_csv('dataprocessing/run_sim.csv',index=False)
#     filtered_street.to_csv('chargingData3.csv',index=False)
#
#
#
#     return "created"













def fair_oriented():
    chargingData = pd.read_csv('chargingData.csv')

    chargingData['startCharging_time'] = pd.to_datetime(chargingData['startCharging_time'])
    chargingData['endCharging_time'] = pd.to_datetime(chargingData['endCharging_time'])
    chargingData['start_time'] = pd.to_datetime(chargingData['start_time'])

    #columns = ['car_id', 'start_time', 'start_lon', 'start_lat', 'end_time',
               #'charging_lon', 'charging_lat', 'T_service', 'T_queue','T_travel']
    columns = ['trip_id', 'start_time', 'startLocation_lon', 'startLocation_lat', 'endCharging_time',
               'charging_longitude', 'charging_latitude', 'startCharging_time', 'ChargingDuration', 'waittime']
    chargingList = []
    #temp_len = len(chargingList)
    #print(chargingData)
    #for i in range(0,len(chargingData)):
    for i in range(0, 50):
        templist = []
        templist.append(chargingData['car_id'][i])
        templist.append(chargingData['start_time'][i])
        templist.append(chargingData['startLocation_lon'][i])
        templist.append(chargingData['startLocation_lat'][i])
        templist.append(chargingData['endCharging_time'][i])
        templist.append(chargingData['charging_longitude'][i])
        templist.append(chargingData['charging_latitude'][i])
        templist.append(chargingData['startCharging_time'][i])
        templist.append(chargingData['ChargingDuration'][i])
        templist.append(chargingData['waittime'][i])
        #return loc
        optimized_loc = find_loc(templist)
        templist[5] = optimized_loc[0]
        templist[6] = optimized_loc[1]
        chargingList.append(templist)
        print("The number of "+str(i))
    with open('chargingData3.csv','w',newline='') as f:
        write = csv.writer(f)

        write.writerow(columns)
        write.writerows(chargingList)
def find_loc(templist):
    start_loc=[templist[2],templist[3]]
    charging_stations = [
        [114.007401, 22.5355],
        [114.0090009, 22.53423323],
        [113.987547, 22.560519],
        [114.088303, 22.562599],
        [114.361504, 22.678499],
        [114.074406, 22.559],
        [113.922977, 22.546375],
        [114.123241, 22.562538],
        [114.101748, 22.582541],
        [114.068837, 22.573326],
        [114.023404, 22.54265],
        [114.023902, 22.619512],
        [113.81775, 22.650682],
        [113.944128, 22.506854],
        [113.941642, 22.527053],
        [113.962844, 22.528519],
        [113.8149322, 22.6513225],
        [114.304419, 22.600844],
        [114.032902, 22.524276],
        [113.85839, 22.579457],
        [113.995054, 22.547247],
        [114.003978, 22.636233],
        [114.045125, 22.55141],
        [113.838486, 22.609576],
        [114.043404, 22.601],
        [113.985199, 22.547701],
        [113.8134, 22.624201],
        [114.135002, 22.544001],
        [114.353401, 22.679399],
        [113.8564, 22.616899],
        [114.031502, 22.5252],
        [114.1798, 22.5585]
    ]
    #status_stations = []
    # for i in range(0,len(charging_stations)):
    #     #0 is status of charge,then add a date
    #     templist = [charging_stations[i],0]
    # T-travel time

    T_travels = []
    for i in range(0,len(charging_stations)):
        T_travel = get_dist_time(start_loc,charging_stations[i])
        T_travels.append(T_travel)
    charging_id = T_travels.index(min(T_travels))
    #T-queue 和 T-service 是否需要计算还是直接用平均值
    #算法的分配是否是一个一个分配的
    # T-queue time(s)
    T_queue = 400

    # T-service time
    T_service = 330
    return charging_stations[charging_id]

#calculate time of travel
def get_dist_time(start_loc,charging_stations):
    gmaps = googlemaps.Client(key='AIzaSyDG6qHspo59jg8SvfACGCWI8By0c7z7d-k')
    now = datetime.now()
    start_coord = "" + str(start_loc[1]) + ", " + str(start_loc[0])
    dest_coord = "" + str(charging_stations[1]) + ", " + str(charging_stations[0])
    directions_result = gmaps.directions(start_coord,dest_coord,mode="driving",avoid="ferries",departure_time=now)
    #value is in second
    return directions_result[0]['legs'][0]['duration']['value']

def main():
    fair_oriented()
    print("finished")
if __name__ == "__main__":
    main()