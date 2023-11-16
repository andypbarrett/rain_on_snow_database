'''Directory of and filepaths for processing data'''
import socket
from typing import Union, List
from pathlib import Path


# Get root data path depending on host
host = socket.gethostname()
if host == "nsidc-617-abarrett":
    AROSS_PATH = Path("/home/apbarret/Data/AROSS/database")  # Needs sorting out
else:
    AROSS_PATH = Path("/projects/AROSS")


# ERA5 Reanalysis path    
ERA5_DATAPATH = AROSS_PATH / "Reanalysis" / "ERA5"
# Path to event packages
EVENT_PATH = AROSS_PATH / "Events"
# Path to Passive Microwave data
PM_PATH = AROSS_PATH / "Passive_microwave"
# Path to Animation data
ANIMATION_PATH = AROSS_PATH / "Animations"
# Path to Surface Observations
SURFOBS_PATH = AROSS_PATH / "observations" / "surface"  # /projects/AROSS is *S*urface
# Path to raw surface observation data
SURFOBS_RAW_PATH = SURFOBS_PATH / "raw"
# Path to concatenated files
SURFOBS_CONCAT_PATH = SURFOBS_RAW_PATH / "all_stations"
# Path to cleaned files
SURFOBS_CLEAN_PATH = SURFOBS_PATH / "clean"
# Path to processed hourly surface observation
SURFOBS_HOURLY_PATH = SURFOBS_PATH / "hourly"
# Path to combined surface obs path
SURFOBS_COMBINED_PATH = SURFOBS_PATH / "combined"
# Paths to ASOS station events database
SURFOBS_EVENTS_PATH = SURFOBS_PATH / "events"

# Reanalysis data extracted for stations
STATIONS_SURFACE_REANALYSIS = ERA5_DATAPATH / 'surface' / 'stations' / 'hourly'
STATIONS_UPPER_AIR_REANALYSIS = ERA5_DATAPATH / 'pressure_levels' / 'stations' / 'hourly'

# IMS Snow cover files
IMS_PATH = AROSS_PATH / 'IMS_Daily_NorthernHemisphere_Snow' / 'original' / '4km'
# ASOS metadata path
ASOS_METADATA_PATH = SURFOBS_PATH / 'metadata' / 'aross.asos_stations.metadata.csv'
# ASOS Winter Rain Counts
ASOS_COUNT_PATH = Path('.')

# File containing event data
EVENT_JSON = "/home/apbarret/src/rain_on_snow/data/Events/events.json"

CLIMATOLOGY_FILES = {
    "surface": ERA5_DATAPATH / "surface" / "daily" / "era5.surface.climatology.daily.nc",
    "temperature": ERA5_DATAPATH / "pressure_levels" / "daily" / "era5.temperature.climatology.daily.nc",
    "geopotential": ERA5_DATAPATH / "pressure_levels" / "daily" / "era5.geopotential.climatology.daily.nc",
    "specific_humidity": ERA5_DATAPATH / "pressure_levels" / "daily" / "era5.specific_humidity.climatology.daily.nc",
    }


def get_station_filepaths(stations: List[str],
                          path: Union[str, Path],
                          all_stations: bool = False,
                          ext: str = '*') -> List[Path]:
    """Returns a list of Path objects to files in path

    Parameters
    ----------
    stations : list of station ids
    path : directory path to files
    all_stations : if True will return all files in path with extension ext
    ext : suffix for file glob

    Returns
    -------
    A list of station files in path with extension extension
    """
    path = Path(path)
    if stations:
        filepaths = [next(path.glob(f"{stn}*{ext}")) for stn in stations]
    elif all_stations:
        filepaths = path.glob(f"*{ext}")
    else:
        raise RuntimeError("stations is empty list and all_stations is False")
    return filepaths

