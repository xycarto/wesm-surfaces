#!/bin/bash

#!/bin/bash

WORKUNIT=$1
STATE=$2
NPROC=$( nproc )
PER=0.8
CALC=$( echo "$NPROC*$PER" | bc )
CORES=$(printf '%.0f' $CALC)

echo ${WORKUNIT}
echo ${STATE}
echo ${NPROC}
echo ${CORES}
