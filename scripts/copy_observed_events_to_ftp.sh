#!/bin/bash

FLAGS='--progress'  # --dry-run'

# Copies netcdf and tiff files to sidads_ftp for Philip Burgess

# List of data packages to copy
SOURCE_PATH=/projects/AROSS/
#SOURCE_FILES=`ls $SOURCE_PATH/*.asos.rain_on_snow.csv`

INCLUDE='{*/Observations/Surface/combine */Observations/Surface/events}'
EXLCUDE='*'

FTP_PATH=/disks/sidads_ftp/pub/incoming/apbarrett/for_michelle

if [ ! -d "$FTP_PATH" ]; then
    echo "$FTP_PATH does not exist"
    echo "   creating..."
    mkdir -p $FTP_PATH
fi

echo "Syncing data packages..."
rsync -avR $FLAGS $SOURCE_PATH/./Observations/Surface/combined $FTP_PATH
rsync -avR $FLAGS $SOURCE_PATH/./Reanalysis/ERA5/surface/stations/hourly $FTP_PATH
rsync -avR $FLAGS $SOURCE_PATH/./Reanalysis/ERA5/pressure_levels/stations/hourly/ $FTP_PATH

ls -l $FTP_PATH
