#!/bin/bash

# bash builds/single-file.sh CA_NoCAL_Wildfires_B1_2018 California test-data/point-clouds/California/CA_NoCAL_Wildfires_B1_2018/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2020n2061.laz

source builds/bash-utils

WORKUNIT=$1
STATE=$2
INFILE=$3

basename=$( basename $INFILE .laz )
dirname=$(dirname $INFILE)
pc=${dirname}/${basename}.laz
# rast=${dirname}/${basename}.tif

make_env $WORKUNIT $STATE

## PROCESSES
make bcm pc=$pc
make tin pc=$pc
make dsm pc=$pc
