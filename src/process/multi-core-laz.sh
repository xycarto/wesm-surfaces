#!/bin/bash

# set -ex ## fail if crash and set to stdout

STATE="California"
WORKUNIT="CA_NoCAL_Wildfires_B1_2018"
DATATYPE="tin"

find data/point-clouds/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P 6 -t -I % make bcm pc=% workunit=$WORKUNIT state=$STATE

## Make TIN
# find data/bcm/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P 12 -t -I % make tin pc=% workunit=$WORKUNIT state=$STATE

# find data/tin/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | xargs -P 12 -t -I % make hillshade tif=% in_dir=tin workunit=$WORKUNIT state=$STATE

# make vrt in_dir=tin workunit=$WORKUNIT state=$STATE

# make vrt in_dir=tin/hillshade workunit=$WORKUNIT state=$STATE

## Make DSM
# find data/bcm/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P 12 -t -I % make dsm pc=% workunit=$WORKUNIT state=$STATE

# find data/dsm/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | xargs -P 12 -t -I % make hillshade tif=% in_dir=dsm workunit=$WORKUNIT state=$STATE

# make vrt in_dir=dsm workunit=$WORKUNIT state=$STATE

# make vrt in_dir=dsm/hillshade workunit=$WORKUNIT state=$STATE

## Make COG

# find data/tin/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | xargs -P 12 -t -I % make reproject tif=% in_dir=tin workunit=$WORKUNIT state=$STATE

# make cog in_dir=tin workunit=CA_NoCAL_Wildfires_B1_2018 state=California
