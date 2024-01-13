#!/bin/bash

source .creds

WORKUNIT=$1
STATE=$2
CORES=$( nproc )

git clone https://${TOKEN}@github.com/xycarto/wesm-surfaces.git

cp -r .creds wesm-surfaces/src/

cd wesm-surfaces/src
make docker-pull
make download-pc workunit=$WORKUNIT state=$STATE
find data/point-clouds/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P $CORES -t -I % make bcm pc=% workunit=$WORKUNIT state=$STATE

exit

