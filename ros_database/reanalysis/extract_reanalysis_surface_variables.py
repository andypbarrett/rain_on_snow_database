"""Extracts reanalysis surface variables for stations"""
import numpy as np

from rain_on_snow.surfaceobs.extract_reanalysis_for_stations import load_stations, extract_surface_variables


def extract_reanalysis_surface_variables(year, reanalysis = 'era5', verbose=False,
                                         clobber=False, oformat="netcdf"):
    """Extracts surface and upper air data for reanalysis pixels that contain ROS stations

    :year: year to extract
    :reanalysis: name of reanalysis - only era5 at the moment
    :verbose: verbose output
    :clobber: overwrite output file
    returns None

    Surface and upper air variables are written to separate files
    """

    # Get station coordiates in lat-lon
    if verbose: print("Loading station metadata")
    longitude, latitude = load_stations()

    if verbose: print(f"Extracting surface variables for stations for {year}")
    extract_surface_variables(year, (latitude, longitude), reanalysis,
                              verbose=verbose, clobber=clobber,
                              oformat=oformat)
  

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog="extract_reanalysis_surface_variables",
        description=("Extract reanalysis surface variables"
                     "for station locations"),
        )
    parser.add_argument("year", type=str,
                        help="year to extract data")
    parser.add_argument("--reanalysis", type=str, default="era5",
                        help="Name of reanalysis - not implemented")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="verbose output")
    parser.add_argument("--clobber", action="store_true",
                        help="overwrite output file")
    parser.add_argument("--oformat", "-o", type=str, default="netcdf",
                        help="Output format")
    args = parser.parse_args()
    
    extract_reanalysis_surface_variables(args.year,
                                         reanalysis=args.reanalysis,
                                         verbose=args.verbose,
                                         clobber=args.clobber,
                                         oformat=args.oformat)
