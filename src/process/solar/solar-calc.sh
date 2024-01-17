#!/bin/bash

DSM=$1
DAY=$2
SOLAR_DIR=$3

base=$( basename $DSM .tif)

solar=${SOLAR_DIR}/$DAY-${base}.tif
#slope=${SOLAR_DIR}/slope-$DAY-${base}

r.in.gdal --overwrite input=${DSM} output=$base

g.region --overwrite raster=$base -p

r.slope.aspect --overwrite elevation=$base aspect=aspect slope=slope -e

r.sun --overwrite elevation=$base horizon_step=30 aspect=aspect slope=slope glob_rad=global_rad day=$DAY time=12

r.out.gdal --overwrite format=GTiff input=global_rad output=${solar}

# r.out.gdal --overwrite format=GTiff input=slope output=${slope}



