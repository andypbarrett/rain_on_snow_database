"""Defines CRS and grid for IMS"""
from pyproj import CRS, Transformer
from affine import Affine

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

grid_transform = Affine(grid_cell_width, 0.0, grid_origin_x,
                        0.0, grid_cell_height, grid_origin_y)


class Grid(Affine):
    """Class for grid operations"""
    def __init__(self,
                 nrow,
                 ncol,
                 grid_cell_width,
                 grid_cell_height,
                 grid_origin_x,
                 grid_origin_y,
                 ):
        self.nrow = nrow
        self.ncol = ncol
        self.grid_cell_width = grid_cell_width
        self.grid_cell_height = grid_cell_height
        self.grid_origin_x = grid_origin_x
        self.grid_origin_y = grid_origin_y

        # Add method to get grid_origin from map origin column
        # and row
        
        # Add set Affine

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
    
                 
def get_xy_coords(xshift=0.0, yshift=0.0):
    """Returns xy coordinatee for the IMS 24 km grid"""
    r0 = 0.5 + yshift
    r1 = nrow + yshift
    c0 = 0.5 + xshift
    c1 = ncol + xshift
    row = np.arange(0.5, nrow)
    col = np.arange(0.5, ncol)
    x, _ = transform * (col, 0.5)
    _, y = transform * (0.5, row)
    return x, y


def get_xarray_spatial_coords():
    """Returns xarray.DataArrays for x and y coordinate"""
    pass
