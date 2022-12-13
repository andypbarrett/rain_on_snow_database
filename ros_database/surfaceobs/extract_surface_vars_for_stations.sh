#!/bin/bash

ybeg=2000
yend=2000

for year in `seq $ybeg $yend`
do
    echo "Extracting surface variables for $year"
    python -m rain_on_snow.surfaceobs.extract_reanalysis_surface_variables $year -v --clobber --oformat zarr
done
