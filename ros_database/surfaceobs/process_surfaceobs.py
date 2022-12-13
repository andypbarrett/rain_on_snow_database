"""Process surface observations files"""

import pandas as pd

from rain_on_snow.filepath import SURFOBS_RAW_PATH
from rain_on_snow.surfaceobs.surface import load_iowa_mesonet_file, get_hourly_obs, wind_speed, wind_direction

country = 'Alaska'
stations = (SURFOBS_RAW_PATH / country).glob('*')

station = 'Bettles-Field'   # For testing


def process_one_file(fp):
    """Processes on file to get hourly cleaned data"""
    df = load_iowa_mesonet_file(fp)
    dfhr = get_hourly_obs(df)
    dfwet = dfhr[dfhr.UP | dfhr.RA | dfhr.FZRA]
    return dfwet


def get_rain_hours(station_path):
    """Returns number of hourly observations with liquid precipitation

    station: Path object to station data
    """
    filelist = station_path.glob('*.txt')
    rain_hours = []
    for fp in filelist:
        df = process_one_file(fp)
        dfrain = df[df.UP | df.RA | df.FZRA]
        rain_hours.append(dfrain)
    df_rain_hours = pd.concat(rain_hours, axis=0)
    df_rain_hours.sort_index(inplace=True)
    return df_rain_hours


'''
For getting rain hours
In [20]: for fp in filepath: 
    ...:     df = process_one_file(fp) 
    ...:     print(df[df.UP | df.RA | df.FZRA]) 
'''

def main():
#    for station in stations
#        nfile = len(list(station.glob('*.txt')))
#        print(f'{station.stem:25s} {nfile}')

    pass


if __name__ == "__main__":
    main()
