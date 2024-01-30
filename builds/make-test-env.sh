#!/bin/bash

# bash builds/make-test-env.sh CA_NoCAL_Wildfires_B1_2018 California 

source builds/bash-utils

WORKUNIT=$1
STATE=$2

make_env $WORKUNIT $STATE


