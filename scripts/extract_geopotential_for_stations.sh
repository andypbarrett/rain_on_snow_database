#!/bin/bash

YBEG=2000
YEND=2003

YEARS=$(seq $YBEG $YEND)

python -m ros_database.reanalysis.extract_reanalysis_for_stations $YEARS --variable geopotential --verbose --clobber
