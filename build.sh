#!/bin/bash

source configs/process-config.env

export PROCESS=$1

make-bcm () {
    CORES=$( nproc )
    PER=0.8
    CALC=$( echo "$NPROC*$PER" | bc )
    cores=$(printf '%.0f' $CALC)

    find $DATA_DIR/point-clouds/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.laz" | \
    xargs -P ${cores} -t -I % \
    make bcm pc=% 
}

make-dsm () {
    CORES=$(nproc)
    find $DATA_DIR/bcm/${STATE}/${WORKUNIT}  -maxdepth 1 -name "*.laz" | \
        xargs -P ${CORES} -t -I % \
        make dsm pc=%

    make vrt 
}

make-tin () {
    CORES=$(nproc)
    find $DATA_DIR/bcm/${STATE}/${WORKUNIT}  -maxdepth 1 -name "*.laz" | \
        xargs -P ${CORES} -t -I % \
        make tin pc=%

    make vrt 
}

make-solar () {
    CORES=$(nproc)
    find $DATA_DIR/dsm/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make solar-average tif=% 

    make vrt  
}

make-hillshade () {
    CORES=$(nproc)
    find $DATA_DIR/${PROCESS}/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make hillshade tif=% 
    make vrt 
}

make-cog () {
    CORES=$(nproc)
    find $DATA_DIR/${PROCESS}/${STATE}/${WORKUNIT} -maxdepth 1 -name "*.tif" | \
    xargs -P ${CORES} -t -I % \
    make cog tif=% 
    make vrt 
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
    git clone --branch $GIT https://${TOKEN}@github.com/xycarto/wesm-surfaces.git
    cp -r .creds wesm-surfaces
    cd wesm-surfaces
    echo -e "PROCESS=$1\n" >> configs/process-config.env
    echo -e "DATA_DIR=$DATA_DIR\n" >> configs/process-config.env
    make download-files 
    if [[ $HS == "true" ]]; then
        make-hillshade
    else
        $processName
    fi

elif [[ $LOCATION = "local" ]]; then
    make download-files 
    if [[ $HS == "true" ]]; then
        make-hillshade
    else
        $processName
    fi
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

