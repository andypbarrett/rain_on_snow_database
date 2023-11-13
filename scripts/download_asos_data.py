#!/bin/python3

from pathlib import Path
from datetime import date

from tqdm import tqdm

from ros_database.mesonet.download_iowas_mesonet import (download_station, OUTPATH,
                                                         get_stations_from_filelist)


def download_asos_data(years=None, stations=None, station_file=None,
                       start=None, end=None,
                       update=True, verbose=False, outpath=None,
                       progress=False):
    """Downloads ASOS records from University of Iowa Mesonet site.

    Data are downloaded for each station by year.  For the current year, records 
    are retrived up to the date of the request

    :years: int, a single year, a list of years to download, or a range of years.
    :start: date to start downloading: expects YYYY-MM-DD
    :end: date to end downloading: expects YYYY-MM-DD or 'now'
    :stations: a list of station ids as str, e.g. PABK
    :station_file: file containing a list of stations.  stations is ignored if 
                   a file is provided
    :update: boolean update station records to current date.  The output path 
             defined in OUTPATH is searched to generate a list of station records to
             update.  If no current files are found in OUTPATH an error is raised.
             years, stations and station_file are ignored if update=True.
    """

    # If both are set, verbose is set to False
    if progress and verbose:
        verbose=False
    
    if not outpath:
        outpath = OUTPATH
    else:
        outpath = Path(outpath)

    if station_file:
        stations = get_stations_from_filelist(station_file)

    # Check that a list of stations has been provided
    if not stations:
        print("No stations provided.  One or more station identifiers must be provided"
              " as a list on the command line or in a file passed to the station_file"
              " keyword argument")
        return

    # Check that the output path exists
    if not outpath.exists():
        print(f"Output directory {outpath} does not exist!\n"
              f"Use -o or --outpath to set valid output path")
        return

    if progress:
        stations = tqdm(stations)
        
    for station in stations:
        if progress: stations.set_description(f"Downloading data for {station}")
        if years:
            for year in years:
                download_station(station, year=year, verbose=verbose, outpath=outpath)
        else:
            download_station(station, start=start, end=end, verbose=verbose, outpath=outpath)

        if verbose & (len(stations) > 1): print("\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=(
        "Downloads ASOS records from University of Iowa Mesonet site.\n"
        "\n"
        "Data are downloaded for each station in the stations list for a single year, "
        "or series of years, or for the date range specified by start and end"
        ))
    parser.add_argument("--year", "-y", type=int, nargs='+',
                        help="Year, or list of years, to download")
    parser.add_argument("--start", type=str, default='1900-01-01',
                        help="Start date for records, default is 1900-01-01. " +
                        "start date is ignored if year is set")
    parser.add_argument("--end", type=str, default=None,
                        help="End data for records.  Default is today's date. " +
                        "end date is ignored if year is set")
    parser.add_argument("--outpath", "-o", type=str, default=None,
                        help="Directory path to save data to")
    parser.add_argument("stations", type=str, nargs="*",
                        default=None,
                        help="List of stations to get record for")
    parser.add_argument("--station_file", type=str, default=None,
                        help=("File containing list ofo stations\n"
                              "Expects one station identifier per line"))
    parser.add_argument("--verbose", action="store_true",
                        help="verbose output")
    parser.add_argument("--progress", action="store_true",
                        help=("displays a progress bar. If progress and verbose are "
                              "both set, verbose is ignored"))

    args = parser.parse_args()
    
    download_asos_data(stations=args.stations, start=args.start, end=args.end,
                       years=args.year, outpath=args.outpath,
                       station_file=args.station_file, verbose=args.verbose,
                       progress=args.progress)

