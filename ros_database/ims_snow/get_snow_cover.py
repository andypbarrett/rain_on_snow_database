"""Extract IMS snow cover data"""

from pathlib import Path
from urllib.error import HTTPError

import gzip
import numpy as np

import fsspec
import rioxarray
import xarray as xr
import pandas as pd
import geopandas
from pqdm.threads import pqdm

from ros_database.ims_snow.load import _build_catalog
from ros_database.ims_snow.ims_crs import IMS24Grid
from ros_database.processing.surface import load_station_metadata

fs = fsspec.filesystem("https")


def read_ims_ascii(filepath, with_header=False):
    """Reads an IMS ASCII data file and returns a numpy.ndarray"""
    nrow = 1024
    ncol = 1024

    # Add an opener lookup function
    
    with gzip.open(filepath, 'r') as f:
        content = f.read().decode("ascii")
    header = [line for line in content.split("\n") if (len(line) > 0) & (len(line) < nrow)]
    data = np.array([list(line) for line in content.split("\n")
                     if len(line) == nrow], dtype=float)
    if with_header:
        return header, data
    else:
        return data


def timestamp_from_filepath(filepath: Path) -> datetime:
    """Parses filepath to get timestamp"""
    m = re.search(r"ims(\d{7}_\d{2})UTC", filepath.name)
    if m:
        time = datetime.strptime(m.groups()[0], "%Y%j_%H")  #.replace(tzinfo=timezone.utc)
    else:
        raise ValueError("Unable to find timestamp-like string in {filepath.name}")
    return time


def load_ascii_grid(f):
    """Loads an IMS ASCII dataset

    Data before 2004 are in ASCII grids

    Parameters
    ----------
    f : file-like object to be passed to reader

    Returns
    -------
    xarray.Dataset with rio accessors
    """
    data = read_ims_ascii(f)

    # Calculate x and y coordinates
    x, y = IMS24Grid.xy_coords()
    # Create x, y coordinates as DataArray
    x = xr.DataArray(x, coords={'x': x}, attrs=IMS24Grid.crs.coordinate_system.to_cf()[0])
    y = xr.DataArray(y, coords={'y': y}, attrs=IMS24Grid.crs.coordinate_system.to_cf()[1])

    # Add coords
    ds = ds.assign_coords(x=x, y=y)
    
    # Extract timestamp from filepath and add as time coordinate
    time = [timestamp_from_filepath(filepath)]
    ds = ds.expand_dims(dim={"time": 1}, axis=0)
    ds["time"] = [timestamp_from_filepath(filepath)]
    ds.time.attrs = {
        "long_name": "time",
        }
    
    # Add CRS
    grid_mapping_name = "ims_polar_stereographic"
    ds.rio.write_crs(IMS24Grid.crs, grid_mapping_name=grid_mapping_name, inplace=True)

    # Add attributes
    attrs = {
        "long_name": "snow and ice cover",
        "standard_name": "area_type",
        "flag_values": [1, 2, 3, 4],
        "flag_meanings": "ice_free_sea snow_free_land lake_ice_or_sea_ice snow",
        "comments": "ice_free_sea includes inland and marine water surfaces",
        }

    global_attrs = {
        "Conventions": "CF-1.11",
        "title": "Northern hemisphere snow and sea ice cover",
        "institution": "US National Ice Center",
        "source": "Interactive Multisensor Snow and Ice Mapping System",
        "history": ("Original files from https://nsidc.org/data/g02156/versions/1: "
                    "Repackaged to NetCDF"),
        "references": "https://nsidc.org/sites/default/files/g02156-v001-userguide_1_1.pdf",
        "comment": "",
        "source_file": f"{filepath}",
        }

    ds.surface_cover.attrs = attrs
    ds = ds.assign_attrs(global_attrs)

    ds.surface_cover.encoding.update({
        "_FillValue": 0,
        "dtype": 'byte',
        "grid_mapping": grid_mapping_name,
        })

    return ds


def extract_from_dataset(ds: xr.Dataset,
                         x: xr.DataArray,
                         y: xr.DataArray) -> pd.DataFrame:
    """Extracts IMS surface values for a set of coordinates from
    an xarray.Dataset

    Parameters
    ----------
    ds : xarray.Dataset
    x : xarray.DataArray containing x coordinates
    y : xarray.DataArray containing y coordinates

    Returns
    -------
    pandas DataFrame
    """
    var_to_drop = ['x','y','projection']
    ims_surface = ds.IMS_Surface_Values.sel(x=x, y=y, method='nearest')
    df = ims_surface.drop_vars(var_to_drop).to_dataframe()
    return df.unstack(level=-1)


def transform_coords(gdf, crs):
    """Transforms x, y coords in gdf to crs and returns x, y
    coordinates as xrray.DataArray objects"""
    return gdf.to_crs(crs).x.to_xarray(), gdf.to_crs(crs).y.to_xarray(), 


def extract_from_file(href: str,
                      coords : geopandas.GeoSeries) -> pd.DataFrame:
    """Extracts IMS surface values for a set of coordinates

    Parameters
    ----------
    href : url or local path to data file
    coords : DataFrame containing geometry column

    Returns
    -------
    pandas DataFrame
    """
    with fs.open(href, compression="gzip") as f:
        with xr.open_dataset(f, decode_coords="all") as ds:
            x, y = transform_coords(coords, ds.rio.crs)
            df = extract_from_dataset(ds, x, y)
    return df
    

def get_station_coords():
    """Returns a GeoPandas.DataFrame containing station locations"""
    stations = load_station_metadata()
    return stations.geometry


def get_href(resolution="4km", format="netcdf"):
    """Returns list of href"""
    return [href for href in _build_catalog(fs, format, resolution).values()]


def get_snow_cover(resolution: str="4km",
                   format: str="netcdf",
                   test: bool=False,
                   ntest: int=10) -> None:
    """Extracts IMS snow cover for stations

    ADD PARAMS
    """

    if resolution == "24km":
        print("Warning: 24km resolution data only available as ascii, "
              "setting format to ascii")
        format = "ascii"
        
    try:
        urls = get_href(resolution, format)
    except HTTPError as err:
        print(f"Search for urls failed: {err}")
    print(href)
    return

    stations = get_station_coords()

    # Use pqdm to parallelize collection of dataframes
    if test:
        urls = urls[:ntest]
    args = [(url, stations) for url in urls]
    list_of_df = pqdm(args, extract_from_file, n_jobs=8, argument_type="args")

#    list_of_df = [extract_from_file(href, stations) for href in urls]

    # Concatenate dataframes 
    df = pd.concat(list_of_df).droplevel(level=0, axis=1)
    print(df.head())

    # Write results
    df.to_csv(f"ims.snow_cover.from_{resolution}.csv")


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser("get_snow_cover",
                                     description=("Extracts snow cover class for "
                                                  "AROSS ASOS stations"))
    parser.add_argument("--resolution", type=str, default="4km",
                        help="data set spatial resolution",
                        choices=["1km", "4km", "24km"])
    parser.add_argument("--format", type=str, default="netcdf",
                        help="file format of data",
                        choices=["netcdf", "ascii"])
    parser.add_argument("--test", action="store_true",
                        help="Run on a subset of urls")
    parser.add_argument("--ntest", type=int, default=10,
                        help="Number of tests")

    args = parser.parse_args()
    
    get_snow_cover(resolution=args.resolution, format=args.format,
                   test=args.test, ntest=args.ntest)
