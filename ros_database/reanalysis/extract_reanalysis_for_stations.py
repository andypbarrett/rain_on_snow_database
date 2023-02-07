'''Extracts surface and upper air data from reanalysis for mesonet stations

TODO:
- combine snow depth, and 10 m u and v winds into surface fields
- add upper air for extraction
'''
import warnings

import matplotlib.pyplot as plt  # For testing
from dask.diagnostics import ProgressBar, Profiler

import numpy as np
import xarray as xr

from ros_database.filepath import ERA5_DATAPATH, STATIONS_SURFACE_REANALYSIS
from ros_database.processing.surface import load_station_metadata


def surface_files_for_year(year):
    """Returns a date sorted list of surface files for a year"""
    pattern = f"era5.surface.{year}????to{year}????.nc"
    filelist = sorted((ERA5_DATAPATH / 'surface' / 'hourly').glob(pattern))
    return filelist


def snowdepth_files_for_year(year):
    """Returns a date sorted list of snow depth files for a year"""
    pattern = f"era5.snow_depth.{year}??????to{year}??????.nc"
    filelist = sorted((ERA5_DATAPATH / 'surface' / 'hourly').glob(pattern))
    return filelist


def u10_files_for_year(year):
    """Returns a date sorted list of snow depth files for a year"""
    pattern = f"era5.10u.{year}??????to{year}??????.nc"
    filelist = sorted((ERA5_DATAPATH / 'surface' / 'hourly').glob(pattern))
    return filelist


def v10_files_for_year(year):
    """Returns a date sorted list of snow depth files for a year"""
    pattern = f"era5.10v.{year}??????to{year}??????.nc"
    filelist = sorted((ERA5_DATAPATH / 'surface' / 'hourly').glob(pattern))
    return filelist


def ta_files_for_year(year):
    """Returns list of hourly air temperature files for a year"""
    pattern = f"era5.temperature.{year}????to{year}????.nc"
    return sorted((ERA5_DATAPATH / 'pressure_levels' / 'hourly').glob(pattern))


def z_files_for_year(year):
    """Returns list of hourly geopotential files for a year"""
    pattern = f"era5.geopotential.{year}????to{year}????.nc"
    return sorted((ERA5_DATAPATH / 'pressure_levels' / 'hourly').glob(pattern))


def q_files_for_year(year):
    """Returns list of hourly specific humidity files for a year"""
    pattern = f"era5.specific_humidity.{year}????to{year}????.nc"
    return sorted((ERA5_DATAPATH / 'pressure_levels' / 'hourly').glob(pattern))


def load_surface_data(year, reanalysis='era5'):
    """Loads surface data.  Snowdepth, and 10 m winds are in separate files, these are
       loaded and combined into a single xarray.Dataset"""
    # Load surface data
    surf_df = xr.open_mfdataset(surface_files_for_year(year), combine='by_coords')

    # Load snow depth
    sd_df = xr.open_mfdataset(snowdepth_files_for_year(year), combine='by_coords')
    surf_df['sd'] = sd_df.SD
    
    # Load 10m u wind
    u10_df = xr.open_mfdataset(u10_files_for_year(year), combine='by_coords')
    surf_df['u10'] = u10_df.VAR_10U
    
    # Load 10m v-wind
    v10_df = xr.open_mfdataset(v10_files_for_year(year), combine='by_coords')
    surf_df['v10'] = v10_df.VAR_10V
    
    return surf_df  # will be xr.concat


def extract_surface_variables(year, stations, reanalysis, verbose=False, clobber=False,
                              oformat='netcdf'):
    """Extracts surface reanalysis variables for stations

    :year: year to extract data
    :stations: tuple of latitude and longitude DataArrays
    :reanalysis: dummy var to allow choice of reanalysis - not implemented
    :clobber: overwrite output file
    """
    fout = STATIONS_SURFACE_REANALYSIS / f"era5.surface.stations.{year}.nc"
    if oformat == "zarr":
        fout = fout.with_suffix(".zarr")

    if fout.is_file() & (not clobber):
        warnings.warn(f"File exists!  Skipping extracting surface variables from {reanalysis} for {year}\n To override set clobber=True",
                      UserWarning)
        return

    if fout.is_file() & clobber:
        fout.unlink()
        
    if verbose: print(f"   Loading surface reanalysis...")
    df = load_surface_data(year, reanalysis=reanalysis)
    
    if verbose: print("   Subsetting data...")
    latitude = stations[0]
    longitude = stations[1]
    sub_df = df.sel(longitude=longitude, latitude=latitude, method='nearest')
    print(sub_df)
    
    if verbose: print("   Computing...")
    with Profiler() as prof, ProgressBar():
        sub_df.load()

    if verbose: print(f"   Writing station subset of surface data to {fout}")
    with ProgressBar():
        if oformat == "zarr":
            sub_df.to_zarr(fout)
        else:
            sub_df.to_netcdf(fout)
    df.close()
    return

    
def load_upper_air_data(year, variable,reanalysis='era5'):
    """Loads an upper air variable for a year"""
    chunks = {"level": 1}
    if variable == "air_temperature":
        df = xr.open_mfdataset(ta_files_for_year(year), chunks=chunks, combine='by_coords')
    elif variable == "geopotential":
        df = xr.open_mfdataset(z_files_for_year(year), combine="by_coords")
    elif variable == "specific_humidity":
        df = xr.open_mfdataset(q_files_for_year(year), combine="by_coords")
    else:
        raise ValueError(f"{variable} is unknown for variable") 
    return df


def extract_upper_air_variable(year, variable, stations, reanalysis,
                                verbose=False, clobber=False):
    """Extracts surface reanalysis variables for stations

    :year: year to extract data
    :stations: tuple of latitude and longitude DataArrays
    :reanalysis: dummy var to allow choice of reanalysis - not implemented
    :clobber: overwrite file if it exists
    """
    ncout = STATIONS_SURFACE_REANALYSIS / f"era5.{variable}.stations.{year}.nc"
    if (not clobber) & ncout.is_file():
        warnings.warn(f"File exists!  Skipping extracting upper air {variable} from {reanalysis} for {year}",
                      UserWarning)
        return

    if verbose: print(f"    Loading {variable}...")
    ds = load_upper_air_data(year, variable, reanalysis=reanalysis)

    if verbose: print("   Subsetting data...")
    latitude = stations[0]
    longitude = stations[1]
    sub_ds = ds.sel(longitude=longitude, latitude=latitude, method='nearest')
    
    if verbose: print("   Computing...")
    with Profiler() as prof, ProgressBar():
        sub_ds.load()

    sub_ds = sub_ds.chunk({"level": 9})

    if verbose: print(f"   Writing station subset of surface data to {ncout}")
    with ProgressBar():
        sub_ds.to_netcdf(ncout)
    return
    ds.close()
    sub_ds.close()
    
    
def load_stations():
    """Returns xarray.DataArray containing latitude and longitude"""
    station_metadata = load_station_metadata()

    # create xr.DataArray objects of lon and lat to allow vectorizd subsetting
    longitude = xr.DataArray(station_metadata['longitude'], dims=['station'],
                             coords=[station_metadata.index])
    latitude = xr.DataArray(station_metadata['latitude'], dims=['station'],
                            coords=[station_metadata.index])
    return longitude, latitude


def extract_reanalysis_for_stations(reanalysis = 'era5', verbose=False,
                                    year_start=2000, year_end=2022,
                                    variable='all', clobber=False):
    """Extracts surface and upper air data for reanalysis pixels that contain ROS stations

    :reanalysis: name of reanalysis - only era5 at the moment
    :verbose: verbose output
    :year_start: year to start extracting data.  Default 2000
    :year_end: year to end extraction.  Default 2022

    returns None

    Surface and upper air variables are written to separate files
    """

    # Get station coordiates in lat-lon
    if verbose: print("Loading station metadata")
    longitude, latitude = load_stations()

    for year in np.arange(year_start, year_end+1):

        if variable in ['all', 'surface']:
            if verbose: print(f"Extracting surface variables for stations for {year}")
            extract_surface_variables(year, (latitude, longitude), reanalysis,
                                      verbose=verbose, clobber=clobber)

        if variable in ['all', 'upper air', 'air temperature']:
            if verbose: print(f"Extract upper air air_temperature for stations for {year}")
            extract_upper_air_variable(year, "air_temperature", (latitude, longitude), reanalysis,
                                       verbose=verbose, clobber=clobber)

        if variable in ['all', 'upper air', 'geopotential']:
            if verbose: print(f"Extract upper air geopotential for stations for {year}")
            extract_upper_air_variable(year, "geopotential", (latitude, longitude), reanalysis,
                                       verbose=verbose, clobber=clobber)

        if variable in ['all', 'upper air', 'specific humidity']:
            if verbose: print(f"Extract upper air specific_humidity for stations for {year}")
            extract_upper_air_variable(year, "specific_humidity", (latitude, longitude), reanalysis,
                                       verbose=verbose, clobber=clobber)


if __name__ == "__main__":
    # TODO
    # Extract script to scripts
    import argparse

    parser = argparse.ArgumentParser(description="Extract surface and upper air fields for Mesonet stations")
    parser.add_argument("year", type=int, nargs="+",
                        help="Single year or list of years")
    parser.add_argument("--variable", type=str, default="all",
                        help="Name of variable or group of variables to extract",
                        choices=['all', 'surface', 'upper air', 'air temperature',
                                 'geopotential', 'specific humidity'])
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    parser.add_argument("--clobber", "-c", action="store_true",
                        help="Overwrite files")
    args = parser.parse_args()

    extract_reanalysis_for_stations(verbose=verbose, year_end=year_end, variable=variable,
                                    clobber=clobber)
