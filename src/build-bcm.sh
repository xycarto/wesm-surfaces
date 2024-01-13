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

find data/point-clouds/California/CA_NoCAL_Wildfires_B1_2018 -name "*.laz" | xargs -P 8 -t -I % make bcm pc=% workunit=CA_NoCAL_Wildfires_B1_2018 state=California