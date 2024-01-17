#!/bin/bash

source .creds

WORKUNIT=$1
STATE=$2
CORES=$( nproc )

git clone --branch solar https://${TOKEN}@github.com/xycarto/wesm-surfaces.git

cp -r .creds wesm-surfaces/src/

cd wesm-surfaces/src
make docker-pull
make download-dsm workunit=$WORKUNIT state=$STATE

## Make SOLAR
find data/dsm/${STATE}/${WORKUNIT} -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make solar-average tif=% workunit=$WORKUNIT state=$STATE

make vrt in_dir=solar workunit=$WORKUNIT state=$STATE


### Make SOALR COGS
find data/solar/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make reproject tif=% in_dir=solar workunit=$WORKUNIT state=$STATE

make cog in_dir=solar workunit=$WORKUNIT state=$STATE

exit

find data/solar/California/CA_NoCAL_Wildfires_B1_2018 -maxdepth 1 -name "*.tif" | \
    xargs -P 5 -t -I % \
    make reproject tif=% in_dir=solar workunit=CA_NoCAL_Wildfires_B1_2018 state=California

    make reproject tif=data/dsm/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2023n2051.tif in_dir=solar workunit=CA_NoCAL_Wildfires_B1_2018 state=California

make cog in_dir=solar workunit=CA_NoCAL_Wildfires_B1_2018 state=California