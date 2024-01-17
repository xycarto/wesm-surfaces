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
    make solar-average pc=% workunit=$WORKUNIT state=$STATE

make vrt in_dir=solar workunit=$WORKUNIT state=$STATE


### Make SOALR COGS
find data/solar/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make reproject tif=% in_dir=dsm workunit=$WORKUNIT state=$STATE

make cog in_dir=solar workunit=$WORKUNIT state=$STATE

exit