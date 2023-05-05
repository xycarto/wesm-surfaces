#!/bin/bash

# time bash path/to/laz.laz 

set -ex ## fail if crash and set to stdout
export RUN=
export RUN_RTILER=

make list-index

make download-laz

cat data/palm-north/list/palmerston-north-laz-index.txt | xargs -P 35 -t -I % make bcm laz=%

cat data/palm-north/list/palmerston-north-laz-index.txt | xargs -P 64 -t -I % make dsm laz=%

cat data/palm-north/list/palmerston-north-laz-index.txt | xargs -P 64 -t -I % make dem laz=%

cat data/palm-north/list/palmerston-north-laz-index.txt | xargs -P 64 -t -I % make chm laz=%

cat data/palm-north/list/palmerston-north-laz-index.txt | xargs -P 64 -t -I % make clip-bf laz=%
