# Repository: HealthyRidePGH

### bikepgh.py
The Python program, called `bikepgh.py` that will access live data from the [HealthyRidePGH website](https://healthyridepgh.com/) and provide answers to specific queries about shared bike availability in the Pittsburgh region.

Invoked as:
```
python3 bikepgh.py baseURL command [parameters]  
```
where baseURL is the prefix URL of the source of the data, and it is typically https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/. This should work with ANY proper baseURL.

### Data Feeds
Assume the baseURL parameter is stored in variable $baseURL. We will use two data feeds from the HealthyRidePGH General Bikeshare Feed Specification (GBFS) data feed, as follows:
* **Station Information**: $station_infoURL = $baseURL+'/station_information.json', which provides for each docking station: station_id, name, latitude
 and longtitude, and the total capacity (e.g., [https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_information.json](https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_information.json)).   

* **Station Status**: $station_statusURL = $baseURL+'/station_status.json', which provides for each station_id how many bikes and how many docks are available at any given time (e.g., [https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_status.json](https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_status.json)).

You can find additional information about the GBFS specification at [https://github.com/NABSA/gbfs](https://github.com/NABSA/gbfs) and about all the available data feeds from HealthyRidePGH at [https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/gbfs.json](https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/gbfs.json).


### Command #1: Total bikes available
The command `total_bikes` will compute how many bikes are currently available over all stations in the entire HealthRidePGH network.

Sample invocation:
```
python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_bikes
```

Sample output of your script (meant to illustrate format only):
```
Command=total_bikes
Parameters=
Output=123
```

### Command #2: Total docks available
The command `total_docks` will compute how many docks are currently available over all stations in the entire HealthRidePGH network.

Sample invocation:
```
python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_docks
```

Sample output of your script (meant to illustrate format only):
```
Command=total_docks
Parameters=
Output=168
```

### Command #3: Percentage of docks available in a specific station
The command `percent_avail` will compute how many docks are currently available for the specified station as a percentage over the total number of bikes and docks available. In this case, the station_id is given as a parameter.

Sample invocation:
```
python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ percent_avail 342885
```

Sample output of your script (meant to illustrate format only):
```
Command=percent_avail
Parameters=342885
Output=76%
```
In our example, the num_bikes_available was 4, the num_docks_available was 13, so the percent available was 13/(4+13), i.e., 76%. You should appropriately round the percentage to be an integer. To simplify things, always round down (floor), i.e., return the highest integer that is not greater than the number you try to round.

### Command #4: Names of three closest HealthyRidePGH stations.
The command `closest_stations` will return the station_ids and the names of the three closest HealthyRidePGH stations based just on latitude and longtitude (of the stations and of the specified location). The first parameter is the latitude and the second parameter is the longtitude.

Sample invocation:
```
python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_stations 40.444618 -79.954707
```

Sample output of your script (meant to illustrate format only):
```
Command=closest_stations
Parameters=40.444618 -79.954707
Output=
342885, Schenley Dr at Schenley Plaza (Carnegie Library Main)
342887, Fifth Ave & S Dithridge St
342882, Fifth Ave & S Bouquet St
```
Note that the output starts on a new line and that the station_id is separated by the name of the station using a comma and a space. You should return one station per line, sorted in increasing distance from the provided lat/long coordinates (i.e., first one is the closest).

In order to compute the distance, you can use the following function:

```
from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))
```

### Command #5: Name of the closest HealthyRidePGH station with available bikes
The command `closest_bike` will return the station_id and the name of the closest HealthyRidePGH station that has available bikes, given a specific latitude and longitude. The first parameter is the latitude and the second parameter is the longitude.

Sample invocation:
```
python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_bike 40.444618 -79.954707
```

Sample output of your script (meant to illustrate format only):
```
Command=closest_bike
Parameters=40.444618 -79.954707
Output=342887, Fifth Ave & S Dithridge St
```

### Command #6: The number of bikes available at a bike station 
The command `station_bike_avail` will return the station_id and the number of bikes available at the station, given a specific latitude and longitude. The first parameter is the latitude and the second parameter is the longitude.

Sample invocation:
```
python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ station_bike_avail 40.444618 -79.954707
```

Sample output of your script (meant to illustrate format only):
```
Command=station_bike_avail
Parameters=40.444618 -79.954707
Output=342887, 4
```


