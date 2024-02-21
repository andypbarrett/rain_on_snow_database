"""Extract IMS snow cover data"""

from pathlib import Path

import fsspec
import xarray as xr
import pandas as pd
import geopandas
from pqdm.processing import pqdm

from ros_database.ims_snow.load import _build_catalog
from ros_database.processing.surface import load_station_metadata

fs = fsspec.filesystem("https")


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


def get_snow_cover(resolution="4km", format="netcdf"):


    urls = get_href()

    stations = get_station_coords()

    list_of_df = [extract_from_file(href, stations) for href in urls]
    df = pd.concat(list_of_df).droplevel(level=0, axis=1)
    print(df.head())
#    df.to_csv(f"ims.snow_cover.from_{resolution}.csv")

if __name__ == "__main__":
    get_snow_cover()
