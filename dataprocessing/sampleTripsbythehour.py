import csv
import requests
import json
import datetime

dropoff_csv = 'filtered_dropoffs_9_12.csv'
pickup_csv = 'filtered_pickups_9_12.csv'
dropoff_hour_csv = 'hour_pickup'
pickup_hour_csv = 'hour_dropoff'

driveMode = "driving"
bikeMode = "bicycling"
DTZ_API_KEY = "AIzaSyDLnF0RwcwqWQtnZwyjwe0V0qJjmJmnH1c"
JXM_API_KEY = "AIzaSyAbJsA8HEWB8X50nD_rH_vcwt84D4588Ww"
skip = 100
hourstart=0
hourend=1


def convertToDatetime(x):
    xList = x.split()
    dateList = xList[0].split('/')
    month = int(dateList[0])
    day = int(dateList[1])
    year = int(dateList[2])
    timeList = xList[1].split(":")
    hour = int(timeList[0])
    minute = int(timeList[1])
    AMPM = xList[2]
    if AMPM=='PM' and hour!=12:
        hour += 12
    elif AMPM=='AM' and hour==12:
        hour-=12
    dt = datetime.datetime(year = year,month = month,day = day,hour = hour,minute = minute)
    return dt

def isBetween(dt,startHr,startMin,endHr,endMin):
    if dt.time() > datetime.time(startHr,startMin):
        if dt.time() < datetime.time(endHr,endMin):
            return True
    return False 

untilSkip = skip
perhourcount=[0]*24
with open(dropoff_csv, 'rt') as dropoffs:
    dropoffReader = csv.reader(dropoffs)
    for dropoffRow in dropoffReader:
        if untilSkip > 0:
            untilSkip-=1
            continue
        tripID = dropoffRow[0]
        dropoffTime = dropoffRow[1]
        dropoffAddress = dropoffRow[2]
        dropoffLong = dropoffRow[3]
        dropoffLat = dropoffRow[4]
        with open(pickup_csv,'rt') as pickups:
            pickupReader = csv.reader(pickups)
            for pickupRow in pickupReader:
                if pickupRow[0] == tripID:
                    pickupTime = pickupRow[1]
                    pickupAddress = pickupRow[2]
                    pickupLong = pickupRow[3]
                    pickupLat = pickupRow[4]
                    pickup = convertToDatetime(pickupTime)
                    dropoff = convertToDatetime(dropoffTime)
                    for x in range(0,23):      
                        if isBetween(pickup,x,0,x+1,0):
                            if(perhourcount[x]<=50):
                                dropCSV = open(dropoff_hour_csv+str(x)+".csv",'a',newline='')
                                dropWriter = csv.writer(dropCSV)
                                dropWriter.writerow(dropoffRow)
                                pickCSV = open(pickup_hour_csv+str(x)+".csv",'a', newline='')
                                pickWriter = csv.writer(pickCSV)
                                pickWriter.writerow(pickupRow)
                                perhourcount[x]+=1
                    break
        print("Total: "+str(perhourcount))
        truecount=0
        for x in range(0,23):
            if(perhourcount[x]>50):
               truecount=truecount+1
        if(truecount==24):
               break
        




