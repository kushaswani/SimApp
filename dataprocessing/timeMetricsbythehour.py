import csv
import requests
import json
import datetime

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

def calculateTimeDifference(pickupTime,dropoffTime):
    difference = dropoffTime - pickupTime
    return difference.total_seconds()



dropoff_csv = 'filtered_dropoffs_9_12.csv'
pickup_csv = 'filtered_pickups_9_12.csv'
dropoff_hour_csv = 'byhours/hour_pickup'
pickup_hour_csv = 'byhours/hour_dropoff'

driveMode = "driving"
bikeMode = "bicycling"
DTZ_API_KEY = "AIzaSyDLnF0RwcwqWQtnZwyjwe0V0qJjmJmnH1c"
JXM_API_KEY = "AIzaSyAbJsA8HEWB8X50nD_rH_vcwt84D4588Ww"
api_key = DTZ_API_KEY

totalMapsDriveTime = 0
totalMapsDriveDist = 0
totalMapsBikeTime = 0
totalMapsBikeDist = 0
totalTaxiTime = 0
tripCount = 0

for x in range(0,23):
    with open(dropoff_hour_csv+str(x)+".csv", 'rt') as dropoffs:
        dropoffReader = csv.reader(dropoffs)
        for dropoffRow in dropoffReader:
            tripID = dropoffRow[0]
            dropoffTime = dropoffRow[1]
            dropoffAddress = dropoffRow[2]
            dropoffLong = dropoffRow[3]
            dropoffLat = dropoffRow[4]
            with open(pickup_hour_csv+str(x)+".csv",'rt') as pickups:
                pickupReader = csv.reader(pickups)
                for pickupRow in pickupReader:
                    if pickupRow[0] == tripID:
                        pickupTime = pickupRow[1]
                        pickupAddress = pickupRow[2]
                        pickupLong = pickupRow[3]
                        pickupLat = pickupRow[4]
                        rDrive = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+pickupAddress+"&destinations="+dropoffAddress+"&mode="+driveMode+"&key="+api_key)
                        rBike = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+pickupAddress+"&destinations="+dropoffAddress+"&mode="+bikeMode+"&key="+api_key)
                        resultBike = json.loads(rBike.text)
                        resultDrive = json.loads(rDrive.text)
                        if resultDrive['rows'][0]['elements'][0]['status'] != 'OK' or resultBike['rows'][0]['elements'][0]['status'] != 'OK':
                            print("status: NOT FOUND")
                            print("\n")
                            break
                        mapsDriveDuration = resultDrive['rows'][0]['elements'][0]['duration']['value']
                        mapsBikeDuration = resultBike['rows'][0]['elements'][0]['duration']['value']
                        mapsDriveDist = resultDrive['rows'][0]['elements'][0]['distance']['value']
                        mapsBikeDist = resultBike['rows'][0]['elements'][0]['distance']['value']
                        pickupDT = convertToDatetime(pickupTime)
                        dropoffDT = convertToDatetime(dropoffTime)
                        driveDuration = calculateTimeDifference(pickupDT,dropoffDT)
                        totalMapsDriveTime += mapsDriveDuration
                        totalMapsDriveDist += mapsDriveDist
                        totalMapsBikeTime += mapsBikeDuration
                        totalMapsBikeDist += mapsBikeDist
                        totalTaxiTime += driveDuration
                        tripCount=tripCount+1
                        break
                    if(tripCount>50):
                        break
        print("hours:"+str(x))
        print("Drive Time: "+str(mapsDriveDuration))
        print("Drive Dist: "+str(mapsDriveDist))
        print("Bike Time: "+str(mapsBikeDuration))
        print("Bike Dist: "+str(mapsBikeDist))
        print("Taxi Time: "+str(driveDuration))
        print("--------------------------");
        print("Drive Total Time: "+str(totalMapsDriveTime))
        print("Drive Total Dist: "+str(totalMapsDriveDist))
        print("Bike Total Time: "+str(totalMapsBikeTime))
        print("Bike Total Dist: "+str(totalMapsBikeDist))
        print("Taxi Total Time: "+str(totalTaxiTime))
        print("Trip count: "+str(tripCount))
        print("\n")
        totalMapsDriveTime = 0
        totalMapsDriveDist = 0
        totalMapsBikeTime = 0
        totalMapsBikeDist = 0
        totalTaxiTime = 0
        tripCount = 0


