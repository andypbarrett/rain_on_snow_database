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

### Data cleaning
- remove duplcate records
- decode WXCODE and convert units
- aggregate to create hourly records.

### Extracting precipitation events



## Recreating or updating the database

If necessary, the database can be recreated using the following workflow and scripts

1. Download the metadata and data from IEM
   - python -m ros_database.mesonet.make_mesonet_metadata
   - To update the metadata set `--clobber` flag.
   
Add NSF badge