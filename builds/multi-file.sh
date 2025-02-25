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
# ### Make Slopes
# for d in "dem" "dsm" "chm"; do
#     cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make slope tif=data/${d}/${STATE}/${WORKUNIT}/%
# done

# ### Make Hillshades
# for d in "dem" "dsm" "chm"; do
#     cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make hillshade tif=data/${d}/${STATE}/${WORKUNIT}/%
# done

# ### Make Solar
# cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make solar-average tif=data/dsm/${STATE}/${WORKUNIT}/%

### Make COG
for d in "dem" "dsm" "chm" "solar"; do
    cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make reproject tif=data/${d}/${STATE}/${WORKUNIT}/%
    make cog in_dir=data/${d}/${STATE}/${WORKUNIT}/
done

for d in "dem" "dsm" "chm"; do
    cat data/lists/${WORKUNIT}.txt | xargs -P $CORES -t -I % make reproject tif=data/${d}/${STATE}/${WORKUNIT}/hillshade/%
    make cog in_dir=data/${d}/${STATE}/${WORKUNIT}/hillshade
done