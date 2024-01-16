#!/bin/bash

# bash merge-index.sh California

WORKUNIT=$1
STATE=$2

if test -f data/hexbin/${STATE}/${WORKUNIT}/${WORKUNIT}-hexbin-merged.gpkg; then
  rm data/hexbin/${STATE}/${WORKUNIT}/${WORKUNIT}-hexbin-merged.gpkg
fi

if test -f data/hexbin/${STATE}/${WORKUNIT}/${WORKUNIT}-hexbin-merged-tmp.gpkg; then
  rm data/hexbin/${STATE}/${WORKUNIT}/${WORKUNIT}-hexbin-merged-tmp.gpkg
fi

ogrmerge.py -overwrite_ds -f GPKG -o data/hexbin/${STATE}/${WORKUNIT}/${WORKUNIT}-hexbin-merged-tmp.gpkg data/hexbin/${STATE}/${WORKUNIT}/*.gpkg
ogr2ogr -nlt PROMOTE_TO_MULTI data/hexbin/${STATE}/${WORKUNIT}/${WORKUNIT}-hexbin-merged.gpkg data/hexbin/${STATE}/${WORKUNIT}/${WORKUNIT}-hexbin-merged-tmp.gpkg