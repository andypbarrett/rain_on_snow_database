"""Updates filenames to reflect period of record in file"""

import datetime as dt
import re
from pathlib import Path

from scripts.clean_asos_data import get_raw_station_filepaths

from ros_database.filepath import SURFOBS_RAW_PATH
from ros_database.processing.surface import read_mesonet_raw_file


def get_first_and_last_record_dates(f):
    """Returns a tuple of first and last record in file"""
    df = read_mesonet_raw_file(f)
    first_record = df.index.min()
    last_record = df.index.max()
    return first_record, last_record


def get_modification_datetime(f):
    """Returns datetime object for file modification time"""
    return dt.datetime.fromtimestamp(f.stat().st_mtime)


def make_filestem(stem, first_record, last_record):
    """Returns filepath with first and last record dates"""
    return re.sub("(?<=to)[0-9]{8}", last_record.strftime("%Y%m%d"),
                  re.sub("[0-9]{8}(?=to)", first_record.strftime("%Y%m%d"), stem))


def fix_raw_filenames():
    """changes filename for raw files to have first and last record as dates"""

#    raw_path = Path("/home/apbarret/Data/AROSS/database/observations/surface/test_rename")
    raw_path = SURFOBS_RAW_PATH
    
    filepaths = get_raw_station_filepaths([], raw_path, True)

    for fp in filepaths:
        first_record, last_record = get_first_and_last_record_dates(fp)
        newstem = make_filestem(fp.stem, first_record, last_record)
        newpath = fp.with_stem(newstem)
        print(f"Renaming {fp.name} --> {newpath.name}")
        fp.rename(newpath)
    return


if __name__ == "__main__":
    fix_raw_filenames()
