"""Creates a KML file containing database stations"""

import pandas as pd
import fiona

from ros_database.processing.surface import load_station_metadata

fiona.supported_drivers['KML'] = 'rw'

def make_ge_kml():
    """Creates KML file"""
    stations = load_station_metadata()

    with fiona.drivers():
    # Might throw a WARNING - CPLE_NotSupported in b'dataset sample_out.kml
    # does not support layer creation option ENCODING'
        stations.to_file('data/aross_asos_stations.kml', driver='KML')


if __name__ == "__main__":
    make_ge_kml()
