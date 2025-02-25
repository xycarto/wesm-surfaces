#!/bin/bash

source ../.creds

WORKUNIT=$1
STATE=$2
PROCESS=$3  
TYPE=$6
LOCATION=$7
CORES=$( nproc )

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


# ## Make TINS
# find data/bcm/${STATE}/${WORKUNIT} -name "*.laz" | \
#     xargs -P ${CORES} -t -I % \
#     make tin pc=% workunit=$WORKUNIT state=$STATE

# find data/tin/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
#     xargs -P ${CORES} -t -I % \
#     make hillshade tif=% in_dir=tin workunit=$WORKUNIT state=$STATE

# make vrt in_dir=tin workunit=$WORKUNIT state=$STATE

# make vrt in_dir=tin/hillshade workunit=$WORKUNIT state=$STATE

# ### Make TIN COGS
# find data/tin/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
#     xargs -P ${CORES} -t -I % \
#     make reproject tif=% in_dir=tin workunit=$WORKUNIT state=$STATE

# find data/tin/${STATE}/${WORKUNIT}/hillshade -maxdepth 1 -name "*.tif" | \
#     xargs -P ${CORES} -t -I % \
#     make reproject tif=% in_dir=tin/hillshade workunit=$WORKUNIT state=$STATE

# make cog in_dir=tin workunit=$WORKUNIT state=$STATE

# make cog in_dir=tin/hillshade workunit=$WORKUNIT state=$STATE

# ## Make DSM
# find data/bcm/${STATE}/${WORKUNIT} -name "*.laz" | xargs -P ${CORES} -t -I % make dsm pc=% workunit=$WORKUNIT state=$STATE

# find data/dsm/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | xargs -P ${CORES} -t -I % make hillshade tif=% in_dir=dsm workunit=$WORKUNIT state=$STATE

# make vrt in_dir=dsm workunit=$WORKUNIT state=$STATE

# make vrt in_dir=dsm/hillshade workunit=$WORKUNIT state=$STATE

# ### Make DSM COGS
# find data/dsm/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
#     xargs -P ${CORES} -t -I % \
#     make reproject tif=% in_dir=dsm workunit=$WORKUNIT state=$STATE

# find data/dsm/${STATE}/${WORKUNIT}/hillshade -maxdepth 1 -name "*.tif" | \
#     xargs -P ${CORES} -t -I % \
#     make reproject tif=% in_dir=dsm/hillshade workunit=$WORKUNIT state=$STATE

# make cog in_dir=dsm workunit=$WORKUNIT state=$STATE

# make cog in_dir=dsm/hillshade workunit=$WORKUNIT state=$STATE

exit