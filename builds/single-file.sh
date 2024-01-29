#!/bin/bash

# bash builds/single-file.sh CA_NoCAL_Wildfires_B1_2018 California test-data/point-clouds/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2020n2061.laz

WORKUNIT=$1
STATE=$2
INFILE=$3

env_file=configs/process-config.env
basename=$( basename $INFILE .laz )
dirname=$(dirname $INFILE)

pc=${dirname}/${basename}.laz
# rast=${dirname}/${basename}.tif

## Make ENV file
if [ -f $env_file ]; then
    rm $env_file
fi

touch $env_file
echo WORKUNIT=$WORKUNIT >> $env_file
echo STATE=$STATE >> $env_file

## PROCESSES
make bcm pc=$pc
make tin pc=$pc
make dsm pc=$pc
