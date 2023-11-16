"""Create and hourly time series from sub-hourly data"""

from typing import List, Union
from pathlib import Path

from ros_database.processing.make_mesonet_hourly_series import clean_to_hourly

from ros_database.filepath import SURFOBS_CLEAN_PATH, SURFOBS_HOURLY_PATH


def make_hourly_series(stations: Union[str, List[str]],
                       all_stations: bool = False,
                       clean_path: Union[str, Path] = SURFOBS_CLEAN_PATH,
                       outpath: Union[str, Path] = SURFOBS_HOURLY_PATH,
                       verbose: bool = False,
                       progress: bool = False):
    """Resamples cleaned files to an hourly time series

    Parameters
    ----------
    stations : list or str of one or more stations
    all_stations : set to true to process all stations in clean_path
    clean_path : path to cleaned data files (Default {SURFOBS_CLEAN_PATH})
    outpath : path to write hourly files (Default {SURFOBS_HOURLY_PATH})
    verbose : verbose output
    progress : display progress bar.  If verbose and progress both set, verbose is ignored
    """

    # Add function to generate filelist, make common to all scripts

    # Add tdqm
    return

    for fp in clean_path.glob("*.clean.csv"):
        if verbose: print(f"Resampling {fp.stem} to hourly series")
        clean_to_hourly(fp, verbose=verbose)
    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resample cleaned files to hourly data")
    parser.add_argument("stations", type=str, nargs="*",
                        help="list of station ids to process")
    parser.add_argument("--all_stations", action="store_true",
                        help="Resample all stations in clean path")
    parser.add_argument("--clean_path", type=str, default=SURFOBS_CLEAN_PATH,
                        help=f"Path to cleaned files (Default {SURFOBS_CLEAN_PATH}")
    parser.add_argument("--outpath", type=str, default=SURFOBS_HOURLY_PATH,
                        help=f"Path to write resampled files (Default={SURFOBS_HOURLY_PATH}")
    parser.add_argument("--verbose", action="store_true",
                        help="verbose output")
    parser.add_argument("--progress", action="store_true",
                        help=("display progress bar.  If both verbose and progress set, "
                              "verbose is ignored"))
    
    args = parser.parse_args()
    
    make_hourly_series(args.stations, all_stations=args.all_stations,
                       clean_path=args.clean_path, outpath=args.outpath,
                       verbose=args.verbose, progress=args.progress)
