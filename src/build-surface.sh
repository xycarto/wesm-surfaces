#!/bin/bash

source .creds

WORKUNIT=$1
STATE=$2
CORES=$( nproc )

git clone https://${TOKEN}@github.com/xycarto/wesm-surfaces.git

cp -r .creds wesm-surfaces/src/

cd wesm-surfaces/src
make docker-pull
make download-bcm workunit=$WORKUNIT state=$STATE

## Make TINS
find data/bcm/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P ${CORES} -t -I % make tin pc=% workunit=$WORKUNIT state=$STATE

find data/tin/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | xargs -P ${CORES} -t -I % make hillshade tif=% in_dir=tin workunit=$WORKUNIT state=$STATE

make vrt in_dir=tin workunit=$WORKUNIT state=$STATE

make vrt in_dir=tin/hillshade workunit=$WORKUNIT state=$STATE

exit