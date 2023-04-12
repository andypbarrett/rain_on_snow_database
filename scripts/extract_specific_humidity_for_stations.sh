#!/bin/bash

YBEG=2004
YEND=2022

YEARS=$(seq $YBEG $YEND)

python -m ros_database.reanalysis.extract_reanalysis_for_stations $YEARS --variable specific_humidity --verbose --clobber
