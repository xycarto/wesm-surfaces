#!/bin/bash

source ../.creds

PROCESS=$3  
TYPE=$6
CORES=$( nproc )
PER=0.8
CALC=$( echo "$NPROC*$PER" | bc )
CORES=$(printf '%.0f' $CALC)

if [[ $TYPE != "test" ]]; then
    source .creds
    git clone https://${TOKEN}@github.com/xycarto/wesm-surfaces.git
    cp -r .creds wesm-surfaces/src/
    cd wesm-surfaces/src
    make docker-pull
fi

make download-files workunit=$WORKUNIT state=$STATE process=$PROCESS type=$TYPE

# find data/point-clouds/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P $CORES -t -I % make bcm pc=% workunit=$WORKUNIT state=$STATE

exit

