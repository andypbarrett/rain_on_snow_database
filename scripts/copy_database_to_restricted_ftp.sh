#!/bin/bash

DATABASE_VERSION="version_2.0.0"

SRC="$HOME/Data/AROSS/database/observations/surface/$DATABASE_VERSION/"

TARGET_HOST="apbarret@$NSIDC_APBARRETT"
TARGET="$TARGET_HOST:/disks/restricted_ftp/aross/database/$DATABASE_VERSION"

ARGS="-avzu"

EXCLUDE=""

if [ -n "$EXCLUDE" ]; then
    ARGS="$ARGS --exclude $EXCLUDE"
fi

echo "#############################################################################################################"
echo "# Copying database                                                                                          #"
echo "#   Source: $SRC"
echo "#   Target: $TARGET"
echo "#############################################################################################################"

time rsync $ARGS $SRC $TARGET
