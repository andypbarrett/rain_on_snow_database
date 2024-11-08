"""Finds stations that have measured precipitation and are on land
in IMS dataset.  Results are written to a json file"""

import pandas as pd

from ros_database.filepath import SURFOBS_HOURLY_PATH
from ros_database.processing.surface import load_station_combined_data

import json

# Find stations with precipitation
stations_with_precipitation = {}
for fp in SURFOBS_HOURLY_PATH.glob("*.csv"):
    df = load_station_combined_data(fp)
    if df.p01i.any():
        stations_with_precipitation[df.station.iloc[0]] = fp

# Find stations with snow on land in IMS
ims_snow = pd.read_csv("ims.surface_values.stations.csv", index_col=0)
island = ims_snow.isin([4,2]).all()
land_stations = island[island]

# Find set intersection
land_stations_with_precipitation = {}
for id in set(land_stations.index).intersection(set(stations_with_precipitation.keys())):
    land_stations_with_precipitation[id] = str(stations_with_precipitation[id])
land_stations_with_precipitation

# Write to json
with open("data/land_stations_with_precipitation.json", "w") as f:
    json.dump(dict(sorted(land_stations_with_precipitation.items())), f)

