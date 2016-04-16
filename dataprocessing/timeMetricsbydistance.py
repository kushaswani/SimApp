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


morning_dropoff_csv = 'rep_dropoffs_morning_9_12.csv'
morning_pickup_csv = 'rep_pickups_morning_9_12.csv'
afternoon_dropoff_csv = 'rep_dropoffs_afternoon_9_12.csv'
afternoon_pickup_csv = 'rep_pickups_afternoon_9_12.csv'
evening_dropoff_csv = 'rep_dropoffs_evening_9_12.csv'
evening_pickup_csv = 'rep_pickups_evening_9_12.csv'
dropoff_csv = morning_dropoff_csv
pickup_csv =morning_pickup_csv
driveMode = "driving"
bikeMode = "bicycling"
DTZ_API_KEY = "AIzaSyDLnF0RwcwqWQtnZwyjwe0V0qJjmJmnH1c"
JXM_API_KEY = "AIzaSyAbJsA8HEWB8X50nD_rH_vcwt84D4588Ww"
api_key = JXM_API_KEY   
totalMapsDriveTime = [0]*15
totalMapsDriveDist = [0]*15
totalMapsBikeTime = [0]*15
totalMapsBikeDist = [0]*15
totalTaxiTime =[0]*15
tripCount = [0]*15
totalDriveTime=[0]*15
totalDriveDist=[0]*15
totalMapsBikeTime=[0]*15
totalTaxTime=[0]*15

def isBetween(dt,dist1,dist2):
    if dt>dist1:
        if dt <=dist2:
            return True
    return False


with open(dropoff_csv, 'rt') as dropoffs:
    dropoffReader = csv.reader(dropoffs)
    for dropoffRow in dropoffReader:
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
                    for y in range(0,15):   #sorts things into the right bucket
                        if(isBetween(mapsDriveDist,y*500,(y+1)*500)):
                           if(tripCount[y]<=30):
                                totalMapsDriveTime[y] += mapsDriveDuration
                                totalMapsDriveDist[y] += mapsDriveDist
                                totalMapsBikeTime[y] += mapsBikeDuration
                                totalMapsBikeDist[y] += mapsBikeDist
                                totalTaxiTime[y] += driveDuration
                                tripCount[y]=tripCount[y]+1
                    print(tripCount)
                    break

for x in range(0,15):
    print("Range:"+str(x*500))
    print("Drive Total Time: "+str(totalMapsDriveTime[x]))
    print("Drive Total Dist: "+str(totalMapsDriveDist[x]))
    print("Bike Total Time: "+str(totalMapsBikeTime[x]))
    print("Bike Total Dist: "+str(totalMapsBikeDist[x]))
    print("Taxi Total Time: "+str(totalTaxiTime[x]))
    print("Trip count: "+str(tripCount[x]))
    print("\n")
    

