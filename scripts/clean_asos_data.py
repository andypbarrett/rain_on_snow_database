"""Loads data for a single station for period of record, removes duplicate entries
and performs unit conversions

Remove duplicates
Remove rows where all NaN, except ID
Convert to SI units
"""
import warnings
import shutil

from pathlib import Path

from tqdm import tqdm

import pandas as pd
import numpy as np

from ros_database.processing.clean_mesonet_data import clean_iowa_mesonet_asos_station
from ros_database.filepath import SURFOBS_RAW_PATH, SURFOBS_CLEAN_PATH

TEST_STATIONS = ['BGPT.20050101to20140724.txt',
                 'CYLT.19870305to20231020.txt',
                 'CYAB.20110113to20231021.txt',
                 'PAFM.19880105to20231022.txt',
                 'EFET.19980419to20231022.txt',
                 'BGAA.20010721to20140724.txt',
                 'ESNX.19770701to20231022.txt',
                 'ULAA.19310104to20230501.txt',
                 'ENAT.19730101to20231022.txt',
                 'EFHA.19730101to20231022.txt',
                 'ESSD.19790802to20231022.txt',
                 'UHMA.19331201to20231022.txt',
                 'PALP.20020119to20231022.txt',
                 'BIEG.19490101to20231022.txt',
                 'BIAR.19310103to20231022.txt',
                 'ENAL.19730101to20231022.txt']


# Suppresses FutureWarning about conflict in how strings and scalars are compared
# see: https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
# Using
# python                    3.7.6           h8356626_5_cpython    conda-forge
# numpy                     1.18.4           py37h8960a57_0    conda-forge
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_raw_station_filepaths(stations, raw_path, all_stations):
    """Returns a list of Path objects to raw station files"""
    raw_path = Path(raw_path)
    if stations:
        filepaths = [next(raw_path.glob(f"{stn}*.txt")) for stn in stations]
    elif all_stations:
        filepaths = raw_path.glob("*.txt")
    else:
        raise RuntimeError("stations is empty list and all_stations is False")
    return filepaths


def clean_mesonet_data(stations, all_stations=False, raw_path=None, outpath=None,
                       create_outpath=False, ignore_fill_warnings=False,
                       verbose=False, progress=False, testing=False):
    """Cleans raw data for stations in stations list if provided or for all stations in 
    raw_path if all_stations set to True.  Cleaned files are written to outpath.

    raw station file names are expected to have the format IIII.yyyymmddtoyyyymmdd.txt, 
    where IIII is the 4 letter station id, and yyyymmdd are the dates for the first and
    last records in the file.

    Parameters
    ----------
    stations : list[str]
        List of station ids to clean
    all_stations : bool P
        Process all stations in raw_path.  
    raw_path : str
        Path to raw mesonet files.  Default is None.  Will use SURFOBS_RAW_PATH.  See
        ros_database.filepath.py
    outpath : str
        Path to output file.  Default is None.  Will use SURFOBS_CLEAN_PATH.  See
        ros_database.filepath.py
    create_outpath : bool
        Create outpath, if outpath does not exist.
    ignore_fill_warnings : bool
        Ignore fill warnings from pandas.
    verbose : bool
        Show verbose output
    progress : bool
        Show progress bar.  If verbose and progress are both set, verbose if ignored.
    testing : bool
        Test on a subset of stations

    Returns
    -------
    None
    """

        
    if progress and verbose:
        verbose = False
        
    # Get filepaths for raw files
    if testing:
        # Just for testing. So that cleaning is duplicating old cleaned files
        filepaths = [SURFOBS_RAW_PATH / fp for fp in TEST_STATIONS]
    else:
        try:
            filepaths = get_raw_station_filepaths(stations, raw_path, all_stations)
        except RuntimeError as err:
            print("Either a list of station ids must be given or all_stations flag set")
            print(err)
            return

    if not outpath.exists():
        if create_outpath:
            print(f"Creating {outpath}")
            outpath.mkdir()
        else:
            print(f"Directory for cleaned data {outpath} does not exist\n"
                  "Either create output directory or et create_outpath flag "
                  "to create automatically")

    if progress:
        filepaths = tqdm(filepaths)

    if verbose: print("Cleaning mesonet observation data")
    for fp in filepaths:
        if verbose: print(f"Cleaning {fp}")
        if progress: filepaths.set_description(f"Cleaning {fp}")
        clean_iowa_mesonet_asos_station(fp, verbose=verbose,
                                        ignore_fill_warnings=ignore_fill_warnings)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cleans raw IOWA Mesonet ASOS station files\n"
                                      "removes duplicate records, parses records and "
                                     "converts units")
    parser.add_argument("stations", type=str, nargs="*",
                        help="List of station ids to clean")
    parser.add_argument("--all_stations", action="store_true",
                        help="Clean all stations in raw_path")
    parser.add_argument("--ignore_fill_warnings", help="silence warnings", action="store_true")
    parser.add_argument("--raw_path", type=str, default=SURFOBS_RAW_PATH,
                        help=("Path to directory containing raw station files. "
                              f"By default will search for files in {SURFOBS_RAW_PATH}. "
                              "See ros_database.filepath.py to set SURFOBS_RAW_PATH"))
    parser.add_argument("--outpath", type=str, default=SURFOBS_CLEAN_PATH,
                        help=("Directory path for cleaned files. "
                              f"By default will write cleaned files to {SURFOBS_CLEAN_PATH}. "
                              "See ros_database.filepath.py to set SURFOBS_CLEAN_PATH"))
    parser.add_argument("--create_outpath", action="store_true",
                        help="Create outpath if it doesn't exist")
    parser.add_argument("--verbose", help="verbose output", action="store_true")
    parser.add_argument("--progress", action="store_true",
                        help=("displays a progress bar. If progress and verbose are "
                              "both set, verbose is ignored"))
    parser.add_argument("--testing", action="store_true",
                        help="Run on a set of test stations")

    args = parser.parse_args()
    clean_mesonet_data(args.stations, all_stations=args.all_stations,
                       raw_path=args.raw_path, outpath=args.outpath,
                       create_outpath=args.create_outpath,
                       ignore_fill_warnings=args.ignore_fill_warnings,
                       verbose=args.verbose, progress=args.progress,
                       testing=args.testing)
