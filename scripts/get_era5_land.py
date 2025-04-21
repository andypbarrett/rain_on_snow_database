from typing import List
import calendar
from pathlib import Path
import argparse

import cdsapi

ARCTIC = [90, -180, 45, 180]

ALL_HOURS = [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ]
FORECAST_HOURS = [
    "00:00", "06:00", "12:00", "18:00",
    ]

def make_filepath(year, month, outdir="."):
    return Path(outdir) / f"era5_land.snow.{year}.{month:02d}.nc"


def get_days(year, month):
    nday = calendar.monthrange(year, month)[1]
    return [f"{n:02d}" for n in range(1,nday+1)]


def get_era5_land(
        year: int,
        month: int,
        area: List=ARCTIC,
        outdir="."):

    target = make_filepath(year, month, outdir=outdir)
    
    dataset = "reanalysis-era5-land"
    request = {
        "variable": [
            "snow_cover",
            "snow_depth",
#            "land_sea_mask"
        ],
        "year": f"{year}",
        "month": f"{month:02d}",
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30"
        ],
        "time": FORECAST_HOURS,
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": area
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request, str(target))


if __name__ == "__main__":
    year = 2020
    month = 4
    
    get_era5_land(year, month)
