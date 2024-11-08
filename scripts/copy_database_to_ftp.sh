#!/bin/bash

##########################################################
# Copy database on Andy's local machine to restricted ftp.
#
# This requires CU VPN to be activated.
#
# TODO
# 1. Create master script to push database to both ftp
#    and /projects/AROSS
# 2. Add checksum to ensure copy is correct
##########################################################

# Arguments and Options
# Database version
DATABASE_VERSION="version_2.0.0"

# If you want dry run set this to true
#DRYRUN="true"
DRYRUN="false"

# Add files or paths to exclude
EXCLUDE=""

# Source path for database
SRC="$HOME/Data/AROSS/database/observations/surface/./$DATABASE_VERSION/"

# Target host and path
TARGET_HOST="apbarret@$NSIDC_APBARRETT"
FTP_PATH="/disks/restricted_ftp/aross/database/"
TARGET="$TARGET_HOST:$FTP_PATH"

ARGS="-avzu --progress --relative"

if [ "$DRYRUN" = "true" ]; then
    ARGS="$ARGS --dry-run"
fi
    
if [ -n "$EXCLUDE" ]; then
    ARGS="$ARGS --exclude $EXCLUDE"
fi

echo "#############################################################################################################"
echo "# Copying database                                                                                          #"
echo "#   Source: $SRC"
echo "#   Target: $TARGET"
echo "#############################################################################################################"

time rsync $ARGS $SRC $TARGET
