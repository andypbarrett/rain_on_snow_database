"""Plots Alaska liquid preipitation counts"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import pandas as pd


def main():

    stations = pd.read_csv('ak_asos_stations.csv', index_col=0, header=0)
    liquid = pd.read_csv('alaska.liquid_and_freezing_counts.csv', index_col=0, header=0)

    liquid.merge(stations, left_index=True, right_index=True)


    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection=ccrs.Mercator())

    map_extent = (-178, -135, 46, 73)
    ax.set_extent(map_extent, ccrs.PlateCarree())

    ax.coastlines()

    plt.show()
    

if __name__ == "__main__":
    main()
