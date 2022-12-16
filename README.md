# rain_on_snow_database
Code and metadata for Arctic Rain on Snow Study (AROSS) rain on snow database

Data are extracted from the University of Iowa Mesonet (IEM) ASOS site
https://docs.google.com/document/d/1G3NfVtqHXUOrkxR7QzbONhEyO1yEVnys-2jaG14awhI/edit?pli=1#heading=h.p8r294b9jv7e

ADC Guidelines for submitting data
https://arcticdata.io/submit/

## Recreating or updating database

If necessary, the database can be recreated using the following workflow and scripts

1. Download the metadata and data from IEM
   - python -m ros_database.mesonet.make_mesonet_metadata
   - To update the metadata set `--clobber` flag.
   
