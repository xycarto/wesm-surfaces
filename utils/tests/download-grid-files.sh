#!/bin/bash

# bash tests/download-grid-files.sh tahoe-2018-10n

WORKUNIT=$1

list=$( cat "lists/${WORKUNIT}_grid.txt" ) 

for i in ${list[@]}
do
    aws s3 cp --recursive --profile synth s3://synth-chm/${i} $i
done