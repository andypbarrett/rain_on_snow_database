"""Recreates ASOS metadata file from Iowa Environmental Mesonet metadata holdings"""
from __future__ import print_function

import requests
from urllib.request import urlopen

from bs4 import BeautifulSoup
import io

import json
import time
import datetime as dt
from pathlib import Path
import re


import pandas as pd

from ros_database.filepath import ASOS_METADATA_PATH


networks = [
    'AK_ASOS', 'CA_NU_ASOS', 'CA_NT_ASOS', 'CA_YT_ASOS', 'CA_QC_ASOS', 'CA_NF_ASOS', 'FI__ASOS',
    'GL__ASOS', 'IS__ASOS', 'NO__ASOS', 'RU__ASOS', 'SE__ASOS'
]
stations = [
    'PALP', 'PAFM', 'PAKP', 'PANC', 'PANV', 'PARC', 'PABR', 'PABE', 'PABT', 'PABV', 'PABL', 'PAVA',
    'PACV', 'PASC', 'PADE', 'PAEG', 'PAEI', 'PAZK', 'PAFA', 'PFYU', 'PABI', 'PAGA', 'PAGL', 'PAGK',
    'PAHL', 'PAIM', 'PALG', 'PAKV', 'PAEN', 'PAIK', 'PAKN', 'PADQ', 'PAOT', 'PAKK', 'PFKW', 'PADM',
    'PAMC', 'PAIN', 'PAMY', 'PAMH', 'PAMO', 'PANA', 'PANN', 'PAFS', 'PAWN', 'PAOM', 'PFNO', 'PAOR',
    'PAQT', 'PAAQ', 'PPIZ', 'PAAD', 'PARY', 'PARS', 'PASA', 'PACM', 'PASK', 'PAWD', 'PAHX', 'PFSH',
    'PAGH', 'PASL', 'PASX', 'PASV', 'PATK', 'PATA', 'PATE', 'PAOO', 'PAVD', 'PAFB', 'PAIW', 'PAWS',
    'PAWM', 'PAWR', 'PAYA', 'CYLT', 'CYAB', 'CYEK', 'CYBK', 'CYCB', 'CYTE', 'CYCS', 'CYCY', 'CYZS',
    'CWEU', 'CYHK', 'CWGZ', 'CYUX', 'CYGT', 'CYFB', 'CYLC', 'CYBB', 'CYXP', 'CYIO', 'CYVM', 'CYRT',
    'CYUT', 'CYRB', 'CYYH', 'CYKD', 'CYVL', 'CZFM', 'CYFS', 'CYSM', 'CYHY', 'CYEV', 'CYCO', 'CYLK',
    'CYVQ', 'CYPC', 'CYRA', 'CYSY', 'CYUB', 'CYWE', 'CYZF', 'CYDB', 'CYDA', 'CZFA', 'CYMA', 'CYOC',
    'CYZW', 'CYQH', 'CYXY', 'CYPH', 'CYVP', 'CYPX', 'CYYR', 'CYDP', 'EFET', 'EFHA', 'EFHK', 'EFIV',
    'EFJY', 'EFKI', 'EFKE', 'EFKT', 'EFKK', 'EFKU', 'EFKS', 'EFLP', 'EFMA', 'EFMI', 'EFOU', 'EFPO',
    'EFRO', 'EFSA', 'EFSI', 'EFTP', 'EFTU', 'EFUT', 'EFVA', 'BGAA', 'BGPT', 'BGGH', 'BGJN', 'BGKK',
    'BGMQ', 'BGBW', 'BGCO', 'BGQQ', 'BGSS', 'BGSF', 'BGTL', 'BGUK', 'BGUQ', 'BIAR', 'BIEG', 'BIKF',
    'BIRK', 'ENAL', 'ENAT', 'ENAN', 'ENDU', 'ENBS', 'ENBR', 'ENBV', 'ENBO', 'ENBN', 'ENFL', 'ENHF',
    'ENEV', 'ENHK', 'ENKR', 'ENKB', 'ENNA', 'ENMH', 'ENML', 'ENOL', 'ENRO', 'ENSR', 'ENSK', 'ENSB',
    'ENTC', 'ENVA', 'ENSS', 'UHMA', 'ULAA', 'UESO', 'UOII', 'USHH', 'UOHH', 'USRK', 'ULKK', 'UHMM',
    'UERR', 'ULMM', 'USMM', 'USNN', 'UOOO', 'USMU', 'ULPB', 'UHMP', 'UHMD', 'USDD', 'USRR', 'UUYY',
    'UEST', 'UUYH', 'UUYS', 'UERP', 'UEEE', 'ESNX', 'ESSD', 'ESNG', 'ESUT', 'ESNQ', 'ESNK', 'ESPA',
    'ESNL', 'ESUD', 'ESKM', 'ESNO', 'ESNZ', 'ESUP', 'ESNS', 'ESSA', 'ESNN', 'ESND', 'ESST', 'ESNU',
    'ESCM', 'ESOW', 'ESPE', 'ESNV'
]


def parse_original_metadata():
    """Legacy routine that parses an old version of the metadata file and
       returns a list of networks and a list of station identifiers"""
    original_metadata = pd.read_csv(ASOS_METADATA_PATH, index_col=0)
    networks = original_metadata["iem_network"].unique()
    stations = original_metadata.index.unique().values
    return networks, stations


def remove_multiple(c, alist): 
    m = re.match("|".join(alist), c) 
    if m:
        return c.replace(m.group(0), "") 
    else:
        return c 

    
def get_mesonet_network_metadata_json(network, stations=None):
    """Gets a GeoJSON object containing metadata for a mesonet network

    N.B. This is used to get richer metadata.  However, the coordinates for the Point objects
    are only to 4 decimal places and are less precise than those scraped from the html using 
    'format=csv'
    """
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


def get_mesonet_network_metadata(network):
    """Gets Iowa mesonet ASOS network metadata in csv format, parses html to get data
    
    N.B. Iowa Mesonet offers a GeoJSON object for this but the coordinates have fewer digits
    than the csv files.  Go figure!
    
    :network:  str of form <ID>_<PV>_ASOS where ID is a country identifier or state identifier 
               for US, and PV is a Canadian Provine identifier or empty str, unless a US network.
               E.g. For US networks will be AK_ASOS - Alaska network.  For a Canadian network it 
               will have the form CA_NU_ASOS for Nunavut.  For the rest of the world it is
               of form FI__ASOS for Finnish network.

    :return: pandas DataFrame.  Returns an empty dataframe if network invalid.  Raises http_error if
             4xx or 5xx recieved.

    Example:

       metadata = get_mesonet_network_metadata("AK_ASOS")
       print(metadata.head())
    """
    uri = f"https://mesonet.agron.iastate.edu/sites/networks.php?network={network}&format=csv"
    response = requests.get(uri)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("pre").contents[0].strip()
    df = pd.read_csv(io.StringIO(table), index_col=0, parse_dates=True)
    return df
    
    
def generate_mesonet_metadata(clobber=False):
    """Generates a new metadata file for the rain on snow observational
    database from metadata held by Iowa Environmental Mesonet (IEM).  This
    script is part of the tools to recreate the database or to update
    metadata files.

    To calls are made to create the final metadata file.  The first
    scrapes metadata from the IEM network pages for each network in
    the networks list.  The second is to get the GeoJSON files via an
    API.  The reason for this is that the GeoJSON files have more
    metadata fields than the csv's obtained by scraping.  However,
    GeoJSON POINT object truncates the latitude and longitude values
    to 4 decimal places.  This affects geolocation accuracy.  So I
    pull boths sets of metadata, drop the duplicated and truncated
    fields from the GeoJSON and then join the pandas.DataFrames to
    create a single metadata DataFrame.

    Keywords
    :clobber: overwrite existing metadata file
    """

    if ASOS_METADATA_PATH.exists() and not clobber:
        print(f"Metadata file found at {ASOS_METADATA_PATH}")
        print("If you wish to overwrite or update the metadata file use:")
        print("    python -m ros_database.mesonet.make_mesonet_metadata --clobber")
        return

    print("Getting metadata from Iowa Environmental Mesonet")

    # Scrape precise lat and lon from IEM network metadata pages
    new_metadata = pd.concat([get_mesonet_network_metadata(network) for network in networks])
    new_metadata = new_metadata.loc[stations]
    new_metadata = new_metadata.rename({'elev': 'elevation',
                                        'lat': 'latitude',
                                        'lon': 'longitude',
                                        'begints': 'record_begins'},
                                       axis=1)

    # Get GeoJSON metadata files
    json_metadata = pd.concat([get_mesonet_network_metadata_json(network) for network in networks])
    json_metadata = json_metadata.loc[stations]
    json_metadata = json_metadata.drop(['elevation', 'sname', 'longitude', 'latitude', 'sid'],
                                       axis=1)

    new_metadata = new_metadata.join(json_metadata)

    print(f"Writing new metadata file to {ASOS_METADATA_PATH}") 
    new_metadata.to_csv(ASOS_METADATA_PATH)


if __name__ == "__main__":
    import argparse

    
    parser = argparse.ArgumentParser(description="Recreate or update Rain "
                                     "on Snow database metadata")
    parser.add_argument('--clobber', action="store_true",
                        help="Overwrite existing metadata file set in ASOS_METADATA_PATH")
    args = parser.parse_args()
    generate_mesonet_metadata(clobber=args.clobber)
