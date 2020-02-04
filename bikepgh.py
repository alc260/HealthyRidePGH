#Ava Chong
#CS 1656 Project 1, Spring 2020

import sys
import pandas as pd
import numpy as np
import json
import csv
from requests import get
import os
import argparse
import math
from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2 - lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

#data feeds
baseURL = sys.argv[1]

station_infoURL = baseURL+'station_information.json'
station_statusURL = baseURL+'station_status.json'

responseInfo = get(station_infoURL) 
tempInfo = (json.loads(responseInfo.content))

#print('Converting to CSV and writing:')
#print(temp)
info_dict = tempInfo['data']['stations']
with open('info.csv', 'w') as outfileInfo:
    writer = csv.writer(outfileInfo)
    writer.writerow(["station_id","name","short_name", "lat", "lon", "region_id", "capacity"])
    for line in info_dict:
	    writer.writerow([line["station_id"], 
            line["name"], 
            line["short_name"],
            line["lat"],
            line["lon"],
            line["region_id"],
            line["capacity"]])

responseStatus = get(station_statusURL)
tempStatus = (json.loads(responseStatus.content))
#print(tempStatus)
status_dict = tempStatus['data']['stations']
with open('status.csv', 'w') as outfileStatus:
    writer = csv.writer(outfileStatus)
    writer.writerow(["station_id","num_bikes_available","num_docks_available", "is_installed", "is_renting", "is_returning", "last_reported"])
    for line in status_dict:
	    writer.writerow([line["station_id"], 
            line["num_bikes_available"], 
            line["num_docks_available"],
            line["is_installed"],
            line["is_renting"],
            line["is_returning"],
            line["last_reported"]])

dfInfo = pd.read_csv('info.csv')
#print(dfInfo)
dfStatus = pd.read_csv('status.csv', index_col ="station_id")
#print(dfStatus)

#Commands
command = sys.argv[2]

if command == 'total_bikes':
    #total bikes
    total_bikes_col = dfStatus['num_bikes_available']
    total_bikes = sum(total_bikes_col)
    print("command = 'total_bikes'")
    print("total bikes = ", total_bikes)
    
elif command == 'total_docks':
    total_docks_col = dfStatus['num_docks_available']
    total_docks = sum(total_docks_col)
    print("command = 'total_docks'")
    print("total docks = ", total_docks)

elif command == 'percent_avail':
    param1 = int(sys.argv[3])
    station_status = dfStatus.loc[param1]
    num1 = station_status["num_bikes_available"]
    num2 = station_status["num_docks_available"]
    avail = math.floor((num2/(num1+num2))*100)
    print("command = 'percent_avail'")
    print("parameters = ", param1)
    #print(station_status)
    print("output = ", avail, "%")

elif command == 'closest_stations':
    lat1 = float(sys.argv[3])
    lon1 = float(sys.argv[4])
    total_docks_col = dfStatus['num_docks_available']
    x = []
    for i in range(len(total_docks_col)): 
        station_info = dfInfo.iloc[i]
        lat2 = float(station_info["lat"])
        lon2 = float(station_info["lon"])
        dist = distance(lat1, lon1, lat2, lon2)
        x.append([dist,i])
        #print(lat1, lon1, lat2, lon2)
    x.sort()
    print("command = 'closes_stations'")
    print("parameters = ", lat1, lon1)
    print("output = ")
    station1 = dfInfo.iloc[int(x[0][1])]
    id1 = station1['station_id']
    name1 = station1['name']
    print(id1, name1)
    station2 = dfInfo.iloc[int(x[1][1])]
    id2 = station2['station_id']
    name2 = station2['name']
    print(id2, name2)
    station3 = dfInfo.iloc[int(x[2][1])]
    id3 = station3['station_id']
    name3 = station3['name']
    print(id3, name3)
    #print(x[0][1])
    #print(x[1][1])
    #print(x[2][1])
    #print(x)


elif command == 'closest_bike':
    lat1 = float(sys.argv[3])
    lon1 = float(sys.argv[4])

    total_docks_col = dfStatus['num_docks_available']
    x = []
    for i in range(len(total_docks_col)): 
        station_info = dfInfo.iloc[i]
        lat2 = float(station_info["lat"])
        lon2 = float(station_info["lon"])
        st_id = int(station_info['station_id'])
        station_name = station_info['name']
        dist = distance(lat1, lon1, lat2, lon2)
        x.append([dist,st_id,station_name])

    x.sort()
    #print(x)
    ind = 0
    for k in range(len(x)):
        station = dfStatus.loc[int(x[k][1])]
        #print(station)
        avail = int(station['num_bikes_available'])
        if avail > 0:
            ind = k
            print("true")
            break
    
    station_id = int(x[ind][1])
    s_name = x[ind][2]
    print("command = 'closest_bike'")
    print("parameters = ", lat1, lon1)
    print("output = ")
    print(station_id, s_name)


elif command == 'station_bike_avail': 
    lat = float(sys.argv[3])
    lon = float(sys.argv[4])

    total_docks_col = dfStatus['num_docks_available']
    ind = 0
    x = []
    for i in range(len(total_docks_col)): 
        station_info = dfInfo.iloc[i]
        lat2 = float(station_info["lat"])
        lon2 = float(station_info["lon"])
        st_id = int(station_info['station_id'])
        if math.isclose(lat,lat2) and math.isclose(lon,lon2):
            ind = i
            break
    print("command = 'station_bike_avail'")
    print("parameters = ", lat, lon)
    print("output = ")

    station = dfStatus.loc[st_id]
    num = station['num_bikes_available']
    
    #print(station)
    print(st_id, num)

else: 
    print("Error: Command invalid")





