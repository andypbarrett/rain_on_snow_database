"""
Test download script to download IOWA mesonet ASOS data
"""
from __future__ import print_function
import json
import time
import datetime as dt
from pathlib import Path

from urllib.request import urlopen

# Number of attempts to download data
MAX_ATTEMPTS = 6
# HTTPS here can be problematic for installs that don't have Lets Encrypt CA
SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"

# TODO Add way to check path has been set.  Notify and set default to .
OUTPATH = Path('/projects/AROSS/Observations/Surface/raw_new/')

def get_station_list(network):
    """Returns a list of stations in a network"""
    uri = f"https://mesonet.agron.iastate.edu/geojson/network/{network}.geojson"
    data = urlopen(uri)
    jdict = json.load(data)
    stations = []
    for site in jdict["features"]:
        stations.append(site["properties"]["sid"])
    return stations


def get_stations_from_filelist(filename):
    """Build a listing of stations from a simple file listing the stations.
    The file should simply have one station per line.
    
    TBD: Add station name as well as id - could be just station inventory list
    """
    stations = []
    for line in open(filename):
        stations.append(line.strip())
    return stations


def create_download_uri(station, start_date, end_date):
    """Create a uri to download data"""
    service = (
        SERVICE +
        "data=all&tz=Etc/UTC&format=comma&latlon=yes&" +
        start_date.strftime("year1=%Y&month1=%m&day1=%d&") +
        end_date.strftime("year2=%Y&month2=%m&day2=%d&") +
        f"%s&station={station}"
        )
    return service



def make_outfilename(station_id, start_date, end_date, outpath):
    """Create a filepath for output

    station : for letter station id
    start_date : datetime.datetime containing start date of record 
    end_date : datetime.datetime containing end date of record
    outpath : pathlib.Path object containing output path
    
    returns : pathlib.Path object containing file path for output
    """
    return outpath / f"{station_id}.{start_date.strftime('%Y%m%d')}to{end_date.strftime('%Y%m%d')}.txt"


def fetch_data(uri):
    """Fetch the data from the IEM
    The IEM download service has some protections in place to keep the number
    of inbound requests in check.  This function implements an exponential
    backoff to keep individual downloads from erroring.
    Args:
      uri (string): URL to fetch
    Returns:
      string data
    """
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            data = urlopen(uri, timeout=300).read().decode("utf-8")
            if data is not None and not data.startswith("ERROR"):
                return data
        except Exception as exp:
            print("download_data(%s) failed with %s" % (uri, exp))
            time.sleep(5)
        attempt += 1

    # TBD raise exception
    print("Exhausted attempts to download, returning empty data")
    return ""


def write_data(data, outfn):
    """Writes data to file"""
    out = open(outfn, "w")
    out.write(data)
    out.close()
    return


def download_station(station, year=None, start="1900-01-01", end=None,
                     outpath='.', verbose=False):
    """Download data for a station for a given time period

    :station: str station identifier e.g. PADK
    :year: int: year to retrieve.  If year is current year, records up 
           to current date are retrived.  Overrides start and end.  Defaults to start end if None
    :start: date to start download
    :end: date to end download or 'now', which downloads up to most recent date 
    :verbose: verbose output
    """
    # timestamps in UTC to request data for
    date_now = dt.datetime.today()
    if year:
        start_date = dt.datetime(year, 1, 1)
        end_date = dt.datetime(year, 12, 31)
    else:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        if end:
            end_date = min(date_now, dt.datetime.strptime(end, "%Y-%m-%d"))
        else:
            end_date = date_now

    uri = create_download_uri(station, start_date, end_date)
    
    if verbose: print(f"Downloading: {station} "
                      f"{start_date.strftime('%Y-%m-%d')} to "
                      f"{end_date.strftime('%Y-%m-%d')}")
    data = fetch_data(uri)
    
    outfn = make_outfilename(station, start_date, end_date, outpath)
    if verbose: print(f"Writing data to {outfn}")
    write_data(data, outfn)
    return
