"""Retrieves station metadata for stations in database"""

from __future__ import print_function
import json
import time
import datetime as dt
from pathlib import Path
import re

from urllib.request import urlopen

import pandas as pd


def remove_multiple(c, alist): 
    m = re.match("|".join(alist), c) 
    if m:
        return c.replace(m.group(0), "") 
    else:
        return c 

    
def get_network_metadata(network, stations=None):
    """Returns a list of stations in a network"""
    uri = f"https://mesonet.agron.iastate.edu/geojson/network/{network}.geojson"
    data = urlopen(uri)
    jdict = json.load(data)
    stations = pd.json_normalize(jdict, record_path=["features"])
    stations = stations.drop(["type", "geometry.type"], axis=1)
    
    stations.columns = [remove_multiple(c, ["properties\.", "geometry\."])
                        for c in stations.columns]

    # Split time_domain into start and end year columns, change to into
    stations["time_domain"] = stations["time_domain"].apply(lambda x: x[1:-1])
    stations[["start_year", "end_year"]] = stations["time_domain"].str.split("-", expand=True)
    stations["start_year"] = stations["start_year"].where(stations["start_year"] != "????",
                                                          -9999)
    stations["end_year"] = stations["end_year"].where(stations["end_year"] != "Now",
                                                      dt.datetime.now().year)
    stations[["start_year", "end_year"]] = stations[["start_year", "end_year"]].astype(int)

    # Split coordinates into lon and lat
    coordinates = pd.DataFrame(stations["coordinates"].to_list(), columns=["longitude", "latitude"])
    stations = pd.concat([stations, coordinates], axis=1)

    stations = stations.drop(["time_domain", "coordinates"], axis=1)
    stations.set_index("id", inplace=True)
    
    return stations


def get_station_metadata():
    network = "CA_NU_ASOS"
    stations = get_network_metadata(network)
    print(stations.head())
    #print(stations.info())

    # Generate a list of networks
    # Subset station list to just stations we use.
    # Compare geolocation
    # Make a pretty map.
        
if __name__ == "__main__":
    get_station_metadata()
