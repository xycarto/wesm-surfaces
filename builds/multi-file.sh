#!/bin/bash

# bash builds/multi-file.sh CA_NoCAL_Wildfires_B1_2018 California 2

source builds/bash-utils

WORKUNIT=$1
STATE=$2
TEST_NUM=$3

CORES=$( nproc )
PER=0.8
CALC=$(echo "var=$CORES;var*=$PER;var" | bc)
bcm_cores=$( printf '%.0f' $CALC )

make_env $WORKUNIT $STATE

make list-files testnum=$TEST_NUM

# make download-files

# cat data/lists/${WORKUNIT}.txt | xargs -P $bcm_cores -t -I % make bcm pc=data/point-clouds/${STATE}/${WORKUNIT}/%

# cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make dsm pc=data/bcm/${STATE}/${WORKUNIT}/%

# cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make dem pc=data/bcm/${STATE}/${WORKUNIT}/%

# cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make chm pc=data/bcm/${STATE}/${WORKUNIT}/%

## Derived Products
cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make slope tif=data/dem/${STATE}/${WORKUNIT}/%