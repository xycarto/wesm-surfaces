#!/bin/bash

source .creds

WORKUNIT=$1
STATE=$2
NPROC=$( nproc )
CORES=$(( $NPROC / 2 ))

git clone https://${TOKEN}@github.com/xycarto/wesm-surfaces.git

cp -r .creds wesm-surfaces/src/

cd wesm-surfaces/src
make docker-pull
make download-pc workunit=$WORKUNIT state=$STATE
find data/point-clouds/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P 4 -t -I % make bcm pc=% workunit=$WORKUNIT state=$STATE

exit

