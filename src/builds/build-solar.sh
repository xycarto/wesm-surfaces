#!/bin/bash

WORKUNIT=$1
STATE=$2
PROCESS=$3  
TYPE=$6
LOCATION=$7

makeSolar () {
    if [[ $TYPE == "test" ]]; then 
        find_dir=test-data/dsm/${STATE}/${WORKUNIT} 
    else 
        find_dir=data/dsm/${STATE}/${WORKUNIT}
    fi
    CORES=$(nproc)
    find ${find_dir} -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make solar-average tif=% workunit=$WORKUNIT state=$STATE type=$TYPE

    make vrt in_dir=solar workunit=$WORKUNIT state=$STATE type=$TYPE
}

## Make SOLAR
if [[ $LOCATION = "remote" ]]; then
    source .creds
    git clone --branch refactor https://${TOKEN}@github.com/xycarto/wesm-surfaces.git
    cp -r .creds wesm-surfaces/src/
    cd wesm-surfaces/src
    make docker-pull
    make download-files workunit=$WORKUNIT state=$STATE process=$PROCESS type=$TYPE location=$LOCATION
elif [[ $LOCATION = "local" ]]; then
    source .creds
    make download-files workunit=$WORKUNIT state=$STATE process=$PROCESS type=$TYPE location=$LOCATION
    makeSolar 

fi




# ## Make SOLAR
# find data/dsm/${STATE}/${WORKUNIT} -name "*.tif" | \
#     xargs -P ${CORES} -t -I % \
#     make solar-average tif=% workunit=$WORKUNIT state=$STATE

# make vrt in_dir=solar workunit=$WORKUNIT state=$STATE


# ### Make SOALR COGS
# find data/solar/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
#     xargs -P ${CORES} -t -I % \
#     make reproject tif=% in_dir=solar workunit=$WORKUNIT state=$STATE

# make cog in_dir=solar workunit=$WORKUNIT state=$STATE

exit

