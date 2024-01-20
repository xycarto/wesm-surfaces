#!/bin/bash

source ../.creds

WORKUNIT=$1
STATE=$2
PROCESS=$3  
TYPE=$6
LOCATION=$7
CORES=$( nproc )
PER=0.8
CALC=$( echo "$NPROC*$PER" | bc )
cores=$(printf '%.0f' $CALC)


if [[ $LOCATION = "remote" ]]; then
    source .creds
    git clone https://${TOKEN}@github.com/xycarto/wesm-surfaces.git
    cp -r .creds wesm-surfaces/src/
    cd wesm-surfaces/src
    make docker-pull
elif [[ $LOCATION = "local" ]]; then
    source ../.creds
    make download-files workunit=$WORKUNIT state=$STATE process=$PROCESS type=$TYPE location=$LOCATION
fi

# find data/point-clouds/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P $cores -t -I % make bcm pc=% workunit=$WORKUNIT state=$STATE

exit

