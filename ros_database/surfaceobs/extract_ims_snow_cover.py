"""Extract IMS snow cover flags for stations used in AROSS rain on snow study"""

import xarray as xr
import pandas as pd

from pyproj import CRS

from rain_on_snow.filepath import IMS_PATH
from rain_on_snow.surfaceobs.surface import load_station_metadata

def load_ims(filepaths):
    """Loads IMS snow cover grids for a time range"""
    return xr.open_mfdataset(filepaths,
                             combine="by_coords")


def ims_filepaths():
    """Returns an iterable of filepaths by year"""
    return IMS_PATH.glob('*')


def get_ims_crs():
    """Retrieves CRS for IMS data"""
    fp = list((IMS_PATH / '2004').glob('*.nc'))[0]
    with xr.open_dataset(fp) as ds:
        proj4 = ds.projection.attrs['proj4']
    return CRS.from_proj4(proj4)


def get_station_coords():
    """Returns station coordinates in IMS crs as DataArrays that can be
    passed to xr.DataArray.sel() for vectorized indexing"""
    gdf = load_station_metadata()
    gdf.to_crs(get_ims_crs(), inplace=True)
    x = xr.DataArray(gdf.geometry.x, dims=['station'],
                     coords={'station': gdf.index})
    y = xr.DataArray(gdf.geometry.x, dims=['station'],
                     coords={'station': gdf.index})
    return x, y


def get_station_snow(filepath, x, y):
    """Helper function to return station snow code

    :returns: pandas dataframe of snow codes"""
    ds = load_ims(filepath.glob('*.nc'))
    return ds.IMS_Surface_Values.sel(x=x, y=y, method='nearest').to_pandas()


def extract_ims_snow_cover():
    """Extract IMS snow cover flags for stations used in AROSS rain on snow study"""

    x, y = get_station_coords()

    df_list = []
    for filepath in sorted(ims_filepaths()):
        print(f"Getting snow cover code for {filepath.name}")
        df_list.append(get_station_snow(filepath, x, y))
    df = pd.concat(df_list)
    print(df)

    # Find sites with seaice codes
    is_seaice = df[df == 3.].any(axis=0)
    sites_with_seaice = is_seaice[is_seaice].index
    print(sites_with_seaice)
    
    df.to_csv('asos_station_snow_from_ims.csv')


if __name__ == "__main__":
    extract_ims_snow_cover()
