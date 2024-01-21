#!/bin/bash

DSM=$1
DAY=$2
EPSG=$3
SOLAR_DIR=$4

base=$( basename $DSM .tif )

GRASS_DIR="grass-$base"

if [ -d ${GRASS_DIR} ];
then
    rm -rf ${GRASS_DIR}
    mkdir ${GRASS_DIR}
    grass -c $EPSG -e ${GRASS_DIR}/GRASS_ENV
else
    mkdir ${GRASS_DIR}
    grass -c $EPSG -e ${GRASS_DIR}/GRASS_ENV
fi

grass ${GRASS_DIR}/GRASS_ENV/PERMANENT --exec bash src/solar/solar-calc.sh $DSM $DAY $SOLAR_DIR

rm -rf $GRASS_DIR