#!/bin/bash

YBEG=2005
YEND=2022

YEARS=$(seq $YBEG $YEND)

python -m ros_database.reanalysis.extract_reanalysis_for_stations $YEARS --variable surface --verbose --clobber
