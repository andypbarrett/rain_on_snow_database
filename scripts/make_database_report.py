"""Generates a report containing temporal range, data coverage and other metrics"""

from typing import Union, List
from pathlib import Path

from tqdm import tqdm

from ros_database.filepath import SURFOBS_HOURLY_PATH, get_station_filepaths


def make_database_inventory(hourly_path: Union[str, Path] = SURFOBS_HOURLY_PATH,
                            progress: bool = False):
    """Generates an inventory file for database

    Parameters
    ----------
    hourly_path : path to hourly data.  (default is {SURFOBS_HOURLY_PATH}).
    progress : display progress bar

    Returns
    -------
    None
    """

    filelist = get_station_filepaths([], hourly_path,
                                     all_stations=True,
                                     ext="hourly.csv")

    if progress:
        filelist = tqdm(filelist)

    
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Creates an inventory for database")

    make_database_inventory()
