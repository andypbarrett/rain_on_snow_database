"""Counts IMS snow and oce cover frequency, and UP, RA and FZRA counts"""

import pandas as pd

from rain_on_snow.filepath import SURFOBS_COMBINED_PATH
from rain_on_snow.surfaceobs.surface import load_station_combined_data

pd.set_option('display.max_rows', None)


def load_data(station): 
    df = load_station_combined_data(station) 
    df['SNOG'] = df.snog == 4.  # Create Boolean for Snow on Ground
    df['ICEC'] = df.snog == 3.  # Create Boolean for Sea Ice
    df['ROS'] = (df.snog == 4.) & (df.RA | df.FZRA)
    return df[['UP', 'RA', 'FZRA', 'SOLID', 'SNOG', 'ICEC', 'ROS']].dropna() 


def get_ims_and_wcode_counts():

    stations = list(SURFOBS_COMBINED_PATH.glob('*.csv')) 

    result_list = []
    for station in stations:
        print(f"Processing {station}")
        name = station.stem.split('.')[0]
        df = load_data(station)
        result = df.mean()  # These are booleans, so mean returns frequency
        result.name = name
        result_list.append(result)

    df_all = pd.DataFrame(result_list)
    df_all.to_csv('ros.ims_and_wxcode.counts.csv')


if __name__ == "__main__":
    get_ims_and_wcode_counts()
