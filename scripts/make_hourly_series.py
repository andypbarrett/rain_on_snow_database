"""Create and hourly time series from sub-hourly data"""

from typing import List, Union
from pathlib import Path

from tqdm import tqdm

from ros_database.processing.make_mesonet_hourly_series import clean_to_hourly

from ros_database.filepath import (SURFOBS_CLEAN_PATH,
                                   SURFOBS_HOURLY_PATH,
                                   get_station_filepaths)


def make_hourly_series(stations: Union[str, List[str]],
                       all_stations: bool = False,
                       clean_path: Union[str, Path] = SURFOBS_CLEAN_PATH,
                       outpath: Union[str, Path] = SURFOBS_HOURLY_PATH,
                       create_outpath: bool = False,
                       verbose: bool = False,
                       progress: bool = False):
    """Resamples cleaned files to an hourly time series

    Parameters
    ----------
    stations : list or str of one or more stations
    all_stations : set to true to process all stations in clean_path
    clean_path : path to cleaned data files (Default {SURFOBS_CLEAN_PATH})
    outpath : path to write hourly files (Default {SURFOBS_HOURLY_PATH})
    create_outpath : if true and outpath does not exist, it is created
    verbose : verbose output
    progress : display progress bar.  If verbose and progress both set, verbose is ignored
    """

    if progress and verbose:
        verbose = False

    try:
        filepaths = get_station_filepaths(stations, clean_path,
                                          all_stations=all_stations,
                                          ext="clean.csv")
    except RuntimeError as err:
        print("Either a list of station ids must be given or all_stations flag set")
        print(err)
        return

    if not outpath.exists():
        if  create_outpath:
            print(f"Creating {outpath}")
            outpath.mkdir()
        else:
            print(f"Directory for hourly series {outpath} does not exist\n"
                  "Either create output directory or set create_outpath flag "
                  "to create automatically")
            return

    if progress:
        filepaths = tqdm(filepaths)

    if verbose: print("Resampling cleaned files to create hourly series")
    for fp in filepaths:
        if verbose: print(f"Resampling {fp.stem}")
        if progress: filepaths.set_description(f"Resampling {fp.name}")
        clean_to_hourly(fp, outpath, verbose=verbose)  # Add args
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
    parser.add_argument("--create_outpath", action="store_true",
                        help="if true and outpath does not exist, create it (default False)")
    parser.add_argument("--verbose", action="store_true",
                        help="verbose output")
    parser.add_argument("--progress", action="store_true",
                        help=("display progress bar.  If both verbose and progress set, "
                              "verbose is ignored"))
    
    args = parser.parse_args()
    
    make_hourly_series(args.stations, all_stations=args.all_stations,
                       clean_path=args.clean_path, outpath=args.outpath,
                       create_outpath=args.create_outpath,
                       verbose=args.verbose, progress=args.progress)
