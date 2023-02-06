# rain_on_snow_database

The repo contains code and metadata used to download and process data,
and generate an Arctic rain on snow database for the NSF funded Arctic
Rain on Snow Study (AROSS).  This project is part of the NSF
Navigating the New Arctic (NNA) program.  The database combines
station weather observations from [Automated Surface Observing
Systems](https://www.weather.gov/asos/) (ASOS), and near-surface and
upper air fields from atmospheric reanalysis systems.  Currently, only
data from ERA5 are included.

Rain on snow events for the purposes of this database are defined as
liquid or freezing precipitation recorded by ASOS stations [more info
on ASOS p-type observations] during periods when ground surfaces are
snow covered.  ASOS stations are located at airfields.  Stations may
not record snow depth or snow on the ground.  Furthermore, airfields
are, almost by definition, exposed.  Little or no snow may be present
at the location of the ASOS station.  However, extensize snow cover
may be present in the surrounding landscape.  We use remotely sensed
snow cover from the 4 km Integrated Mapping System to identify the
presence of snow in the landscape.

Data __will be__ archived at the Arctic Data Center.
ADC Guidelines for submitting data
https://arcticdata.io/submit/

## Workflow

### Download data

Data are downloaded from the [University of Iowa Mesonet (IEM) ASOS
site](https://mesonet.agron.iastate.edu/ASOS/).  We use the download
api but data can be downloaded from their
[gui](https://mesonet.agron.iastate.edu/request/download.phtml).
Python scripts for downloading raw datafiles and metadata are
described below (See Recreating or updating the database).

__Originally data for each station were dowloaded in individual files
for the September to April period, one file for each annual period.
To make file loading easier, and to future-proof code so that it can
be run on files in which data for a multi-year period of record for a
single station can be processed, annual files are concatenated into
one file for each station. These are in the
/PATH/TO/DATABASE/raw/all_stations directory.__

Concatenation is done by `concatenate_station_files.py`
```
$ python -m ros_database.processing.concatenate_station_files
```

### Data cleaning

ASOS data files hosted by the Iowa Mesonet archive can contain
multiple records for the same timestamp.  These duplicates can arise
from repeated transmission of the same data, or corrected or updated
transmissions.  For the purposes of data cleaning, we assume that
valid data values supercede missing data (NaN).

Duplicated records are searched for and removed on a timestamp by
timestamp basis.  This is necessary because multiple unique timestamps
may have the same values, and appear to be duplicated.  Consevutive
duplicated records may be a problem but these are dealt with by a
different process.  He we focus on removing duplicated time records.

Duplicated timestamps are first identified and copied to a separate
DataFrame.  Records with unique timestamps are copied to another
DataFrame.  For each timestamp with duplicate records, the records are
inspected and missing values (NaN) are filled to maximise data
retention, then only one of the duplicate records is retained.  These,
now unique records, are written to a new DataFrame.  This DataFrame is
then concatenated with the initial DataFrame containing unique records
and sorted by time index.  This new unique DataFrame is returned.

- decode WXCODE and convert units
- aggregate to create hourly records.

### Quality Control

Variables are checked to ensure they are within sensible ranges.
Where possible these ranges are chosen to represent the region.

Relative humidity (relh):  
   Minimum:   0.  - physical limit
   Maximum: 105.  - RH relative to e_ice

1 hour Precipitation Iniensity (p01i):
   Minimum:   0.  - logical limit
   Maximum:
   
Pressure Altimeter (alti) https://glossary.ametsoc.org/wiki/Standard_atmosphere:
   Minimum:
   Maximum:
   
Sea Level Pressure (mslp):
   Minimum:  900 hPa  - pressures below 900 hPa are only recorded in hurricanes 
   Maximum: 1090 hPa  - just above highest recorded pressure 1083.3 hPa 

2 m (near-surface) Air Temperature (t2m):
   Minimum: -70 C - based on lowest recorded Arctic temperature -67.8 C Siberia
   Maximum:  50 C - this might need to be adjusted down, I am only looking at winter 

2 m (near-surface) Dew Point Temperature (d2m):
   Minimum: -20 C
   Maximum:  50 C

Wind Speed (wspd)
   Minimum:   0 m/s
   Maximum: 103 m/s - based on highest recorded wind speed from Mt Washington

Wind direction (drct):
   Minimum:   0.  - logical limit
   Maximum: 360.  - logical limit

Zonal and Meridional Wind Speeds (uwnd, vwnd):
   Minimum: -103. m/s
   Maximum:  103.  m/s

Precipitation type from weather codes (UP, RA, FZRA, SOLID) are boolean.


### Extracting precipitation events
- combine with ims
- Extract events


## Recreating or updating the database

If necessary, the database can be recreated using the following workflow and scripts

1. Download the metadata and data from IEM
   - python -m ros_database.mesonet.make_mesonet_metadata
   - To update the metadata set `--clobber` flag.
   
Add NSF badge