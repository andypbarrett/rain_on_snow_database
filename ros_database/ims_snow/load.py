"""Loads IMS snow data from NOAA@NSIDC"""
import re
import datetime as dt
from urllib.parse import urlparse
import json
from pathlib import Path
import warnings

import fsspec
import xarray


URL = "https://noaadata.apps.nsidc.org/NOAA/G02156"  #netcdf/4km"
SEP = "/"

class IMSSnow:
    """Class to search, access, download and read IMS snow data"""

    def __init__(self, load_catalog=True, catalog_id="ims_snow.catalog.json"):
        self._fs = fsspec.filesystem("https")
        self._catalog_id = Path(catalog_id)
        
        if load_catalog:
            if self._catalog_id.exists():
                self._catalog = _load_catalog(self._catalog_id)
            else:
                warnings.warn(f"{self._catalog_id} does not exist.  No catalog entries.\n"
                              "Either set catalog_id in init or use build_catalog to create one")
                self._catalog = None

    def open_file(date, resolution="4km"):
        """Opens a single file for a given data"""
        
    def build_catalog(self, format="netcdf", resolution="4km", temporal=None,
                      save_catalog=False):
        """Build a simple dictionary containing data"""
        self._catalog = _build_catalog(self._fs, format, resolution)
        if save_catalog:
            _write_catalog(self._catalog, self._catalog_id)

    def write_catalog(self):
        _write_catalog(self.catalog, self._catalog_id)
        
    def catalog(self):
        """Return a catalog"""
        if not self._catalog:
            raise AttributeError("Catalog is empty.  Use `build_catalog` to create one")
        return self._catalog

    def get_entry(self, date_str):
        return self._catalog.get(date_str)


def _build_catalog(fs, format, resolution):
    """Builds a catalog for IMA data"""
    url = URL + SEP if not URL.endswith(SEP) else URL
    url = URL + format + SEP + resolution + SEP
    files = [f for f in fs.find(url) if f.endswith('.nc.gz')]  # Only get netcdf.gzip

    cat = {}
    for item in files:
        entry = parse_urlpath(item)
        timestamp, href = list(entry['netcdf']['4km'].items())[0]
        cat[timestamp.strftime("%Y-%m-%d")] = href
    return cat

def _write_catalog(cat, catalog_id):
    with open(catalog_id, "w") as f:
        json.dump(cat, f, indent=4)


def _load_catalog(catalog_id):
    with open(catalog_id, "r") as f:
        catalog = json.load(f)
    return catalog


def parse_filename(fn):
    """Parses the filename to extract date"""
    m = re.search(r"ims(\d{7})_", fn)
    if m:
        return dt.datetime.strptime(m.groups()[0], "%Y%j")
    else:
        raise ValueError(f"Datestring-type pattern not found in {fn}")

def parse_urlpath(f):
    p = urlparse(f)
    format, resolution, year, filename = p.path.split("/")[3:]
    date = parse_filename(filename)
    return {format: {resolution: {date: f}}}


def check_url(url):
    """Raises HTTPError if url does not exist"""
    try:
        urlopen(url)
    except HTTPError as err:
        raise(err)
