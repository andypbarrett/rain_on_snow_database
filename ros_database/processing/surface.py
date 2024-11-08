"""Functions to process surface observations"""
import warnings

from typing import Union, List
from pathlib import Path

import numpy as np

import pandas as pd
import geopandas as gpd

from ros_database.filepath import SURFOBS_RAW_PATH, ASOS_METADATA_PATH


# Update this column list as necessary
USECOLS = [
    'station',
    'valid',
    'tmpf',
    'dwpf',
    'relh',
    'drct',
    'sknt',
    'p01i',
    'alti',
    'mslp',
    'wxcodes',
]


def fahr2cel(x):
    """Converts Fahrenheit to Celsius"""
    return (x - 32.) * 5. / 9.


def inches2mm(x):
    """Converts inches of precip to mm"""
    return x * 25.4


def knots2mps(x):
    """Converts windspeed in knots to m/s, rounds to nearest cm
    TODO: Need to check if this represnts accuracy of sensor"""
    knots_to_mps = 0.514444
    return (x * knots_to_mps)


def u_wind(wspd, drct):
    """Calculate u-wind"""
    return wspd * np.sin(np.radians(drct))


def v_wind(wspd, drct):
    """Calculate v-wind"""
    return wspd * np.cos(np.radians(drct))


def wind_speed(u, v):
    """Calculates windspeed from u and v components"""
    return np.sqrt(u**2 + v**2)


def wind_direction(u, v):
    """Calculates wid direction from windspeed"""
    theta = np.degrees(np.arctan2(u, v))
    return np.where(theta < 0., 360. + theta, theta)


def altitude_to_pressure(alti):
    """Convert barometric altitutude to pressure using the conersion formula

    P_mb = 33.8639 * P_inhg

    where P_inhg is pressure in inches of mercury

    :alti: barometric altitude in inches of mercury

    :returns: pressure in hPa
    """
    return 33.8639 * alti


def parse_precip(s):
    """Converts p01i column to numeric values, sets Trace (T) to ~0.01 inches (0.2 mm)

    See: https://library.wmo.int/doc_num.php?explnum_id=3152
    """
    return pd.to_numeric(s.where(s != 'T', 0.2/25.4))


def convert_dtype(x):
    if not x:
        return ''
    try:
        return float(x)   
    except:        
        return str(x)


def read_mesonet_raw_file(filepath: Union[Path, str],
                          usecols: List[str] = USECOLS) -> pd.DataFrame:
    """Reads a raw mesonet file downloaded from Uni. Iowa mesonet site

    Parameters
    ----------
    filepath : path to raw file
    usecols : list of column names to read from raw file.  Default list is defined
        in usecols. 

    Returns
    -------
    pandas.Dataframe containing raw data and columns defined in USECOLS
    """
    df = pd.read_csv(filepath, index_col='valid', parse_dates=True,
                     usecols=usecols, comment="#",
                     na_values=["M", ""], low_memory=False)
    df.index.rename("datetime", inplace=True)
    return df


def read_iowa_mesonet_file(filepath, usecols=None, index_col=0):
    """Reads a station file from Iowa State Mesonet Archive

    Converters are used to handle mixed data types in p01i.

    NB. A DTypeWarning is raised for one file.  This needs to be dealt with 
    but is currently ignored.  It seems to not have an effect.

    :filepath: path to data file
    :usecols: define which columns to read.  Default is to read all columns
              usecols=USECOLS is used to read raw data.
    :index_col: column to use as index.  Default is 0

    :returns: pandas dataframe
    """
    # Converters for reading combined dtype column only used
    # for raw input data
    if 'raw' in str(filepath.parent):
        converters = {
            "p01i": convert_dtype,
        }
    else:
        converters = None

    df = pd.read_csv(filepath, header=0, index_col=index_col,
                     parse_dates=True, na_values=["M",""],
                     usecols=usecols, converters=converters,
                     low_memory=False)
    df.index.rename('datetime', inplace=True)
    return df


def check_precip_all_zero(s):
    """Check if all elements in precipitation Series are all zero.  Ignores NaN

    :s: pandas Series

    :returns: Boolean
    """
    return (s.dropna() == 0.).all()


def parse_all_zero_precip(s):
    """If p01i (1 hr precipitation intensity) are all zero, replace with NaN

    :s: pandas.Series containing p01i values

    :returns: pandas.Series containing all NaN, or s
    """
    sc = s.copy()
    if check_precip_all_zero(sc):
        sc.loc[:] = np.nan
    return sc.values


def parse_iowa_mesonet_file(df):
    """Converts units to SI and adds columns for liquid, mixed and solid precipitation.

    :df: pandas dataframe containing data from iowa mesonet file

    :returns: pandas dataframe

    Details
    -------
    - Trace precipitation is set to 0.2 mm (0.01" first and then converted to mm)
    - T2m, D2m converted from deg. F to deg. C
    - windspeed converted from knots to m/s
    - Precipitation converted from inches to mm
    - u and v components of wind added
    - wxcode is parsed and new columns for UP (unidentified precipitation), rain,
      freezing rain and snow are added - type Bool

    - tmpf, dwpf, sknt, p01i and wxcodes are dropped
    """
    df['p01i'] = parse_precip(df["p01i"])  # Set Trace to ~0.01 inches 

    df.loc[: , "p01i"] = parse_all_zero_precip(df["p01i"])  # if all zeros change to NaN
    
    # Unit conversions
    df['t2m'] = fahr2cel(df['tmpf']).round(1)  # keep 1 sig fig
    df['d2m'] = fahr2cel(df['dwpf']).round(1)  # --ditto--
    df['wspd'] = knots2mps(df['sknt']).round(2)
    df['p01i'] = inches2mm(df['p01i']).round(1)
    df['psurf'] = altitude_to_pressure(df['alti']).round(1)
    
    df['UP'] = df.wxcodes.str.contains('UP')  # matches Unknown Precipitation
    df['RA'] = df.wxcodes.str.contains('(?<!FZ)RA')  # matchrain but not freezing rain
    df['FZRA'] = df.wxcodes.str.contains('FZRA')  # match freezing rain
    df['SOLID'] = df.wxcodes.str.contains('(?<!BL)SN')  # Matches SN but not BLSN,  ice???

    df['uwnd'] = u_wind(df.wspd, df.drct).round(2)
    df['vwnd'] = v_wind(df.wspd, df.drct).round(2)
    
    df = df.drop(['tmpf', 'dwpf', 'sknt', 'wxcodes', 'alti'], axis=1)

    return df


def load_iowa_mesonet_file(filepath):
    """Reads Iowa Mesonet Archive files, performs unit conversions,
       adds columns distinguishing if liquid or solid precipitation occurred

    :filepath: path to mesonet file

    :returns: pandas DataFrame
    """
    df = read_iowa_mesonet_file(filepath)
    df = parse_iowa_mesonet_file(df)
    return df


def get_hourly_obs(df):
    """Resamples raw data to hourly observations

    Most obs are transmitted just before hour.  Resampling averages obs from
    previous hour where multiple obs available.  For occurrance of liquid and
    solid precipitation, any precipitation of type in preceding hour is reported
    """

    dfhr = df.resample('1H', closed='right', label='right').apply({
        'station': 'first',
        't2m': 'mean',
        'd2m': 'mean',
        'relh': 'mean',
        'uwnd': 'mean',
        'vwnd': 'mean',
        'mslp': 'mean',
        'psurf': 'mean',
        'p01i': 'mean',
        'UP': 'any',
        'RA': 'any',
        'FZRA': 'any',
        'SOLID': 'any',
        })
    dfhr['wspd'] = wind_speed(dfhr.uwnd, dfhr.vwnd)
    dfhr['drct'] = wind_direction(dfhr.uwnd, dfhr.vwnd)

    dfhr = dfhr.drop(['uwnd', 'vwnd'], axis=1)

    dfhr = dfhr.round({
        't2m': 1,
        'd2m': 1,
        'relh': 2,
        'mslp': 1,
        'psurf': 1,
        'p01i': 1,
        'wspd': 2,
        'drct': 1
        })
    return dfhr


def load_iowa_mesonet_for_station(filepath, loadraw=False):
    '''Loads data for a single station

    :filepath: path to directory containing station data

    :returns: concatenated pandas dataframe for all files in station
    '''
    if loadraw:
        usecols = None
    else:
        usecols = USECOLS
    filelist = filepath.glob('*.txt')
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='^Columns.*')
        df = pd.concat([read_iowa_mesonet_file(fp, usecols=usecols) for fp in filelist])
    return df.sort_index()
    

def get_obs_count_distribution_minute(df):
    '''Returns the observation count for 10 minute 
    periods in an hour.

    The "station" column is dropped
    '''
    obs_count = df.groupby(df.index.minute).count()
    return obs_count.drop('station', axis=1)


def station_paths_in_country(country):
    '''Returns a list of filepaths for stations for a given country'''
    if country.title() not in get_country_list():
        raise FileNotFoundError(f'{country.title()} does not exist in {SURFOBS_RAW_PATH}')
    paths = [p for p in (SURFOBS_RAW_PATH / country.title()).glob('*') if p.is_dir()]
    return paths


def get_country_list():
    """Returns list of countries"""
    return [p.name for p in SURFOBS_RAW_PATH.glob('*') if p.is_dir()]


def load_station_metadata():
    """Get coordinates of stations as geopandas DataFrame"""
    df = pd.read_csv(ASOS_METADATA_PATH, header=0, index_col=0)
    geometry = gpd.points_from_xy(df.longitude, df.latitude, crs="EPSG:4326")
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    return gdf


def load_station_combined_data(station_path):
    """Loads files for stations that combine ASOS 
    observations and IMS snow cover

    :station_path: POSIX style path
    
    :return: pandas DataFrame
    """
    return pd.read_csv(station_path,
                       index_col=0, header=0,
                       parse_dates=True,
                       low_memory=False)
    

def load_hourly_observations(fp: Path) -> pd.DataFrame:
    """Loads hourly observation files

    Arguments
    ---------
    fp : path to hourly station file

    Returns
    -------
    Pandas dataframe
    """
    return pd.read_csv(fp, parse_dates=True, index_col=0, low_memory=False)
