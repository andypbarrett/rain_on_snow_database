"""Create files containing precipitation events"""
from typing import Union
from pathlib import Path

from ros_database.processing.surface import load_station_combined_data
from ros_database.processing.extract_precip_events import find_events
from ros_database.filepath import SURFOBS_COMBINED_PATH, SURFOBS_EVENTS_PATH


def make_outpath(fp: Path) -> Path:
    """Generates output path"""
    return SURFOBS_EVENTS_PATH / fp.name.replace('hourly.combined','event')


def make_one_event_file(fp: Path, fout: Path,
                        float_format=".1f") -> None:
    """Makes an event file for one station

    Parameters
    ----------
    fp : filepath for hourly file
    fout : output path for events file

    Returns
    -------
    None
    """

    df = load_station_combined_data(fp)
    event_df = find_events(df)
    
    fout.parent.mkdir(parents=True, exist_ok=True)
    event_df.to_csv(fout)


def make_events_files(verbose: bool=False,
                      test_run: Union[int, None]=None) -> None:
    """Processes hourly surface files into events files

    Parameters
    ----------
    verbose : set to True for verbose output
    test_run : for testing run first test_run=n files

    Returns
    -------
    None
    """

    for i, fp in enumerate(SURFOBS_COMBINED_PATH.glob("*.csv")):
        if verbose: print(f"Processing {fp.name}")
        
        fout = make_outpath(fp)
        if verbose: print(f"Writing events to {fout}\n")
        make_one_event_file(fp, fout)

        if test_run is not None:
            if i > test_run:
                break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=("Makes events files for hourly files in "
                                                  f"{SURFOBS_COMBINED_PATH}"))
    parser.add_argument("--verbose", action="store_true",
                        help="Verbose output")
    parser.add_argument("--test_run", type=int, default=None,
                        help="For testing.  Run first test_run=n files")

    args = parser.parse_args()
    
    make_events_files(verbose=args.verbose, test_run=args.test_run)
