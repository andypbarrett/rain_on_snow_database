from typing import List

import re
from pathlib import Path

from pyproj import CRS, Transformer

import gzip
import numpy as np
import xarray as xr

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from nsidc_projections.grid import to_cartopy


IMSCMAP = ListedColormap([cfeature.COLORS['water'], cfeature.COLORS['land'], 'slategrey', 'yellow'])
IMSNORM = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], ncolors=4, clip=True)

LAND_MASK_CMAP = ListedColormap([cfeature.COLORS['water'], cfeature.COLORS['land']])
LAND_MASK_NORM = BoundaryNorm([-0.5, 0.5, 1.5], ncolors=2, clip=True)

IMSCRS =  ccrs.Stereographic(central_latitude=90., 
                             central_longitude=-80., 
                             true_scale_latitude=60.)


def resolution_from_file(filepath):
    try:
        return re.search(r"_(\d+km)", filepath.name).groups()[0]
    except:
        raise ValueError("No resolution string found in {filepath.name}")

def read_ims_latlon(fp):
    grid_shapes = {
        "1km": (24576, 24576),
        "4km": (6144, 6144),
        "24km": (1024, 1024),
    }
    shape = grid_shapes[resolution_from_file(fp)]
    with gzip.open(fp, mode='rb') as f:
        grid = np.frombuffer(f.read(), dtype="<f4").reshape(shape)
    return grid


def latlon_from_file(resolution="4km"):
    LATLONPATH = Path.home() / "src" / "rain_on_snow_database" / "data" / "test_data"
    latfile = list(LATLONPATH.glob(f"imslat_{resolution}*"))[0]
    lonfile = list(LATLONPATH.glob(f"imslon_{resolution}*"))[0]
    print(latfile, lonfile)
    latitude = read_ims_latlon(latfile)
    longitude = read_ims_latlon(lonfile)
    return latitude, longitude

def true_scale_lat_to_scale_factor(lat):
    return np.cos(np.radians(45.) - np.radians(lat/2.))**2


def plot_ims_snow_and_ice(da: xr.DataArray, 
                          extent: List=None, 
                          title: str="",
                          crs: ccrs.CRS=None,
                          cmap=None,
                          norm=None) -> plt.Axes:
    """Plots IMS snow and ice cover

    Parameters
    ----------
    da : xarray.DataArray with rioxarray accessors
    extent : map extent in projected crs [x0, x1, y0, y1]

    Returns
    -------
    matplotlib.pyplot.Axes instance
    """

    if not crs:
        try:
            crs = to_cartopy(da.rio.crs)
        except Exception as err:
            print("Unable to determine CRS of da, supply one using crs keyword argument")
            raise err

    coastline = cfeature.GSHHSFeature()

#    fig = plt.figure(figsize=(7,7))
    fig = plt.gcf()
    ax = fig.add_subplot(projection=crs)

    if not extent:
        extent = [da.rio.bounds()[i] for i in [0,2,1,3]]

    ax.set_extent(extent, crs)

    ax.add_feature(coastline)

    da_clip = da.rio.clip_box(*np.array(extent)[[0, 2, 1, 3]])
    img = da_clip.plot.imshow(ax=ax, norm=norm, cmap=cmap, add_colorbar=False)

    if title:
        ax.set_title(title)
        
    # Add colorbar
    fig.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.2, 0.075, 0.6])
    cbar = fig.colorbar(
        img,
        cax=cax, orientation='vertical',
        extend='neither',
        spacing='proportional',
        label='',
        ticks=[1, 2, 3, 4],
        shrink=0.75,
    )

    cbar.ax.set_yticklabels(['Sea', 'Land', 'Sea Ice', 'Snow']);
    cbar.ax.tick_params(which="both", length=0.)

    return ax


def get_extent(point, crs, fov=200000.):

    proj_crs = CRS.from_wkt(crs.to_wkt())
    transformer = Transformer.from_crs(4326, proj_crs, always_xy=True)
    px, py = transformer.transform(*point)
    return [px-fov, px+fov, py-fov, py+fov]
