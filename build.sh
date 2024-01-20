#!/bin/bash

source configs/process-config.env

export PROCESS=$1

make-bcm () {
    if [[ $TYPE == "test" ]]; then 
        find_dir=test-data/point-clouds/${STATE}/${WORKUNIT} 
    else 
        find_dir=data/point-clouds/${STATE}/${WORKUNIT}
    fi
    CORES=$( nproc )
    PER=0.8
    CALC=$( echo "$NPROC*$PER" | bc )
    cores=$(printf '%.0f' $CALC)

    find ${find_dir} -name "*.laz" | \
    xargs -P ${cores} -t -I % \
    make bcm pc=% 
}

make-dsm () {
    CORES=$(nproc)
    find $DATA_DIR/bcm/${STATE}/${WORKUNIT}  -name "*.laz" | \
        xargs -P ${CORES} -t -I % \
        make dsm pc=%

    make vrt in_dir=dsm workunit=$WORKUNIT state=$STATE type=$TYPE
}

make-tin () {
    CORES=$(nproc)
    find $DATA_DIR/bcm/${STATE}/${WORKUNIT}  -name "*.laz" | \
        xargs -P ${CORES} -t -I % \
        make tin pc=%

    make vrt in_dir=dsm workunit=$WORKUNIT state=$STATE type=$TYPE
}

make-solar () {
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

set-data-dir () {
    if [[ $TYPE == "test" ]]; then
        export DATA_DIR="test-data"
    else
        export DATA_DIR="data"
    fi
}

## Run Processes
set-data-dir
processName="make-${PROCESS}" 
if [[ $LOCATION = "remote" ]]; then
    git clone --branch refactor https://${TOKEN}@github.com/xycarto/wesm-surfaces.git
    cp -r .creds wesm-surfaces
    cd wesm-surfaces
    echo -e "PROCESS=$1\n" >> configs/process-config.env
    echo -e "DATA_DIR=$DATA_DIR\n" >> configs/process-config.env
    make download-files 
    $processName
elif [[ $LOCATION = "local" ]]; then
    make download-files 
    $processName

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

