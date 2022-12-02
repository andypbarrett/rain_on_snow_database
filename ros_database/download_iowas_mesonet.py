"""
Test download script to download IOWA mesonet ASOS data
"""
from __future__ import print_function
import json
import time
import datetime
from pathlib import Path

from urllib.request import urlopen

# Number of attempts to download data
MAX_ATTEMPTS = 6
# HTTPS here can be problematic for installs that don't have Lets Encrypt CA
SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"

OUTPATH = Path('.')

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



def make_outfilename(station, start_date, end_date):
    """Create a filepath for output"""
    return OUTPATH / f"{station}.{start_date.strftime('%Y')}to{end_date.strftime('%Y')}.txt"


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


def download_station(station, start_date, end_date, verbose=False):
    """Download data for a station for a given time period

    :station: str station identifier e.g. PADK
    :start_date: datetime object, start datetime for download
    :end_date: datetime object, end datetime for download"""

    uri = create_download_uri(station, start_date, end_date)
    
    if verbose: print("Downloading: {station} {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    data = fetch_data(uri)
    outfn = make_outfilename(station, start_date, end_date)
    if verbose: print("Writing data to {outfn}")
    write_data(data, outfn)
    return


def get_asos_data(year):
    """Our main method"""
    # timestamps in UTC to request data for
    station = 'PADK'
    startts = datetime.datetime(year, 1, 1)
    endts = datetime.datetime(year, 12, 31)

    # Write this function
    # stations = get_stations_from_filelist("mystations.txt")

    download_station(station, startts, endts)
    
if __name__ == "__main__":
    year = 2021
    get_asos_data(year)

