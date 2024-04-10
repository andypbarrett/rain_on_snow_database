"""Create files containing precipitation events"""
from pathlib import Path

from ros_database.processing.surface import load_station_combined_data
from ros_database.processing.extract_precip_events import find_events
from ros_database.filepath import SURFOBS_HOURLY_PATH, SURFOBS_EVENTS_PATH


def make_outpath(fp: Path) -> Path:
    """Generates output path"""
    return SURFOBS_EVENTS_PATH / fp.name.replace('hourly','event')


def make_one_event_file(fp: Path, fout: Path) -> None:
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


def make_events_files(verbose=False):
    """Processes hourly surface files into events files"""

    for fp in SURFOBS_HOURLY_PATH.glob("*.csv"):
        if verbose: print(f"Processing {fp.name}")
        
        fout = make_outpath(fp)
        if verbose: print(f"Writing events to {fout}\n")
        make_one_event_file(fp, fout)


if __name__ == "__main__":
    verbose=True
    make_events_files(verbose=verbose)
