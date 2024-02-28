import pytest
import datetime as dt

from ros_database.ims_snow.load import parse_urlpath

@pytest.mark.parametrize("path, expected",
                         [
                             ("https://noaadata.apps.nsidc.org/NOAA/G02156/netcdf/1km/2014/ims2014337_1km_v1.3.nc.gz",
                              {
                                  "netcdf": {
                                      "1km": {
                                          dt.datetime(2014,12,3): "https://noaadata.apps.nsidc.org/NOAA/G02156/netcdf/1km/2014/ims2014337_1km_v1.3.nc.gz"
                                          }
                                      }
                                  }
                              ),
                             ("https://noaadata.apps.nsidc.org/NOAA/G02156/netcdf/4km/2014/ims2014001_4km_v1.2.nc.gz",
                             {
                                 "netcdf": {
                                     "4km": {
                                         dt.datetime(2014,1,1): "https://noaadata.apps.nsidc.org/NOAA/G02156/netcdf/4km/2014/ims2014001_4km_v1.2.nc.gz"
                                         }
                                     }
                                 }
                             ),
                             ("https://noaadata.apps.nsidc.org/NOAA/G02156/24km/1997/ims1997036_00UTC_24km_v1.1.asc.gz",
                              {
                                  "ascii": {
                                      "24km": {
                                          dt.datetime(1997,2,5): "https://noaadata.apps.nsidc.org/NOAA/G02156/24km/1997/ims1997036_00UTC_24km_v1.1.asc.gz"
                                      }
                                  }
                              }
                              ),
                         ]
                        )
def test_parse_urlpath(path, expected):
    entry = parse_urlpath(path)
    print(f"Expected: {expected}")
    print(f"Result: {entry}")
    assert entry == expected
