"""Defines CRS and grid for IMS"""
from typing import Tuple

from pyproj import CRS, Transformer
from affine import Affine
import numpy as np

# Grid and projection parameters are taken from Ims24km.gpd
# Projection Parameters
projection_method = "stere"
central_latitude = 90.
central_longitude = -80.
true_scale_latitude = 60.
map_origin_latitude = 89.998344
map_origin_longitude = 55.000000
radius = 6371200.0
false_easting = -121.487472489721
false_northing = -121.487472489721

# False Easting and False Northing are calculated from map_origin_latitude and
# map_origin_longitude using the following steps.
#
# Step 1. A North Polar Stereographic CRS is defined for the IMS projection parameters
#         without defining false_easting and false_northing
#          proj4_string = (f"+proj={projection_method} +lat_0={central_latitude} "
#                          f"+lat_ts={true_scale_latitude} +lon_0={central_longitude} "
#                          f"+ellps=sphere +R={radius}")
#          NorthPolarStereo = CRS.from_proj4(proj4_string)
#
# Step 2. A transformer is defined to convert geographic coordinates in WGS84 to the
#         North Polar Stereographic CRS
#          transformer = Transformer.from_crs(WGS84, IMSNorthPolarStereo, always_xy=True)
#
# Step 3. false_easting and false_northing are calculated as the offsets of the
#         map_origin_longitude and map_origin_latitude from the north pole (0.,90.).
#          false_easting, false_northing = transformer.transform(map_origin_longitude,
#                                                                map_origin_latitude)

proj4_string = (f"+proj={projection_method} +lat_0={central_latitude} "
                f"+lat_ts={true_scale_latitude} +lon_0={central_longitude} "
                f"+ellps=sphere +R={radius} "
                f"+x_0={false_easting} +y_0={false_northing}")
IMS24NorthPolarStereo = CRS.from_proj4(proj4_string)

# CRS for WGS84
WGS84 = CRS.from_epsg(4326)

WGS84toIMS24NorthPolarStereo = Transformer.from_crs(WGS84, IMS24NorthPolarStereo,
                                                    always_xy=True)

# Grid Parameters for 24 km grid
nrow = 1024
ncol = 1024
grid_cell_width = 23684.997  # meters
grid_cell_height = 23684.997  # meters
grid_map_origin_column = 511.5
grid_map_origin_row = 511.5
grid_origin_x = (grid_map_origin_column + 0.5) * grid_cell_width * -1.
grid_origin_y = (grid_map_origin_row + 0.5) * grid_cell_height * -1.

#grid_transform = Affine(grid_cell_width, 0.0, grid_origin_x,
#                   0.0, grid_cell_height, grid_origin_y)


class Grid():
    """Class for grid operations"""
    def __init__(self,
                 nrow,
                 ncol,
                 grid_cell_width,
                 grid_cell_height,
                 grid_origin_x,
                 grid_origin_y,
                 grid_rotation_x = 0.0,
                 grid_rotation_y = 0.0,
                 crs = None
                 ):
        self.nrow = nrow
        self.ncol = ncol
        self.grid_cell_width = grid_cell_width
        self.grid_cell_height = grid_cell_height
        self.grid_origin_x = grid_origin_x
        self.grid_origin_y = grid_origin_y
        self.grid_rotation_x = grid_rotation_x
        self.grid_rotation_y = grid_rotation_y
        self.crs = crs

        # Add method to get grid_origin from map origin column
        # and row
        
        # Add set Affine
        self.transform = Affine(self.grid_cell_width,
                                self.grid_rotation_y,
                                self.grid_origin_x,
                                self.grid_rotation_y,
                                self.grid_cell_height,
                                self.grid_origin_y)


    def __repr__(self):
        return (f"Grid("
                f"nrow={self.nrow}, "
                f"ncol={self.ncol}, "
                f"grid_cell_width={self.grid_cell_width}, "
                f"grid_cell_height={self.grid_cell_height}, "
                f"grid_origin_x={self.grid_origin_x}, "
                f"grid_origin_y={self.grid_origin_y})")

    def __str__(self):
        return (f"Grid object\n"
                f"    nrow: {self.nrow}\n"
                f"    ncol: {self.ncol}\n"
                f"    grid_cell_width: {self.grid_cell_width}\n"
                f"    grid_cell_height: {self.grid_cell_height}\n"
                f"    grid_origin_x: {self.grid_origin_x}\n"
                f"    grid_origin_y: {self.grid_origin_y}\n")


    def xy_coords(self,
                  xshift: float=0.0,
                  yshift: float=0.0):
        """Returns xy coordinatee for the IMS 24 km grid

        Parameters
        ----------
        xshift : Number of column coordinates to shift x-coordinates to get grid cell corners.
                 -0.5 to get left cell boundary, 0.5 to get right cell boundary.
        yshift : Number of row coordinates to shift y-coordinates to get grid cell corners.
                -0.5 to get lower cell boundary, 0.5 to get upper cell boundary.  Uses sign
                of grid_cell_height to modify yshift to ensure yshift < 0. always gets lower
                cell boundary.

        Returns
        -------
        Tuple of numpy.array

    
        Examples
        --------
        """
        r0 = 0.5 + yshift
        r1 = self.nrow + yshift
        c0 = 0.5 + xshift
        c1 = self.ncol + xshift

        row = np.arange(r0, r1)
        col = np.arange(c0, c1)
        x, _ = self.transform * (col, 0.5)
        _, y = self.transform * (0.5, row)
        return x, y


    def bounds(self):
        """Returns grid bounds"""
        x0, y0 = self.transform * (0., 0.)
        x1, y1 = self.transform * (self.ncol, self.nrow)
        return (min([x0,x1]), min([y0,y1]), max([x0,x1]), max([y0,y1]))


IMS24Grid = Grid(nrow, ncol, grid_cell_width, grid_cell_height,
                 grid_origin_x, grid_origin_y,
                 crs=IMS24NorthPolarStereo)


def get_xarray_spatial_coords():
    """Returns xarray.DataArrays for x and y coordinate"""
    pass
