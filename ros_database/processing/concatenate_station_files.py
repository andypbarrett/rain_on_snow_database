"""Concatenates all files for a single station, creates a new filename with just 
station code identifier and date range.  Note data are still only for winter period.
This file format simplifies loading data and allows complete record download in the future.
"""

from ros_database.processing.surface import (station_paths_in_country,  
                                             load_iowa_mesonet_for_station)
from ros_database.filepath import SURFOBS_RAW_PATH

country_list = ['alaska','canada','finland',
                'greenland', 'iceland', 'norway',
                'russia', 'sweden']

def get_station_paths():
    """Generates a list of file paths for each station as Path objects"""
    return [path for country in country_list for path in station_paths_in_country(country)]

    
def concatenate_station_files(verbose=False):
    """Main function to concatenate files for all stations"""
    for path in get_station_paths():
        print(f"   Loading files from {path}")
        df = load_iowa_mesonet_for_station(path)
        station_id = df.iloc[0,0]
        start_date = df.index[0].strftime("%Y%m%d")
        end_date = df.index[-1].strftime("%Y%m%d")
        outfile = SURFOBS_RAW_PATH / "all_stations" / f"{station_id}.{start_date}to{end_date}.csv"
        print(f"   Writing to {outfile}")
        df.to_csv(outfile)


if __name__ == "__main__":
    concatenate_station_files(verbose=True)
