#!/bin/bash

# bash src/geospatial/data-check.sh tahoe-2018-10n laz_tahoe_tile_-10000_100000_denoised_ground_norm_classify_seamless.laz

WORKUNIT=$1
IN_FILE=$2

check_dir="data/data-check/${WORKUNIT}"
base_name=$(basename $IN_FILE .laz)

dir=(dsm dem chm)

for i in ${dir[@]}
do
    mkdir -p  $check_dir/$i
    aws s3 cp --profile synth s3://synth-chm/data/$i/${WORKUNIT}/${base_name}.tif ${check_dir}/$i/${base_name}.tif
done

aws s3 cp --recursive --profile synth s3://synth-chm/grid/408358 ${check_dir}

