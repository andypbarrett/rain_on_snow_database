from pathlib import Path

import geopandas as gpd

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


DATAFILE = Path("/home") / "apbarret" / "src" / "rain_on_snow" / "data" / "Station_observations" / "ROS_Events_Station_List.kml"
map_proj = ccrs.NorthPolarStereo()


def read_stations_kml():
    """Reads the KML file with station locations"""
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    df = gpd.read_file(DATAFILE, driver='KML')
    return df


def plot_basemap(fig):
    """Creates basemap for plot"""
    ax = fig.add_subplot(projection=map_proj)
    ax.set_extent([-180,180,55,90], ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    #ax.gridlines(ylocs=[66.5], linewidth=2, color='0.5', zorder=0)
    #ax.gridlines()
    return ax


def plot_surface_stations():
    """Creates plot to show surface stations used in ML for ROS"""
    stations_df = read_stations_kml()

    stations_nps_df = stations_df.to_crs(crs=map_proj.proj4_params)

    asos_only_stations = stations_nps_df[(stations_nps_df.Name.str.contains("ASOS")) &
                                         (~stations_nps_df.Name.str.contains("Upper [Aa]ir"))]
    asos_and_upper_air_stations = stations_nps_df[stations_nps_df.Name.str.contains("Upper [aA]ir") &
                                                  stations_nps_df.Name.str.contains("ASOS")]
    upper_air_only_stations = stations_nps_df[stations_nps_df.Name.str.contains("Upper [aA]ir") &
                                              ~stations_nps_df.Name.str.contains("ASOS")]

    fig = plt.figure(figsize=(10,10))
    ax = plot_basemap(fig)
    asos_only_stations.plot(ax=ax, alpha=0.7, color="tab:blue", label="ASOS")
    asos_and_upper_air_stations.plot(ax=ax, alpha=0.7, color="tab:red", label="ASOS and Upper Air")
    upper_air_only_stations.plot(ax=ax, alpha=0.7, color="tab:green", label="Upper Air")
    ax.legend(fontsize=15)

    fig.savefig(Path("figures", "aross_surface_stations_map.png"))
    #plt.show()


if __name__ == "__main__":
    plot_surface_stations()
