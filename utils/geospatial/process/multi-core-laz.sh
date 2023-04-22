#!/bin/bash

# time bash process/multi-core-laz.sh tahoe-2018-10n 

WORKUNIT=$1
cores=$(nproc)

echo ${cores}

## REPLACE THIS WITH A LIST OUTSIDE
python3 process/list-index.py ${WORKUNIT}

# # # # "c5a.8xlarge" Use 10 cores.
# # # # "c5a.16xlarge" Use 25 cores.
aws s3 cp --recursive s3://synth-chm/data/laz/${WORKUNIT} data/laz/${WORKUNIT}

cat lists/${WORKUNIT}.txt | xargs -t -I % -P 25  python3 process/bcm-alt.py %

wait

# rm -r data/laz

cat lists/${WORKUNIT}.txt | xargs -t -I % -P ${cores} python3 process/dsm.py %

cat lists/${WORKUNIT}.txt | xargs -t -I % -P ${cores} python3 process/dem.py %

wait

# rm -r data/bcm

cat lists/${WORKUNIT}.txt | xargs -t -I % -P ${cores} python3 process/chm.py %

wait

python3 gridding/grid-intersect-workunit.py ${WORKUNIT}

cat lists/${WORKUNIT}_grid.txt | xargs -t -I % -P ${cores} python3 gridding/grid-clip-laz.py ${WORKUNIT} % \
|| exit \
|| exit \
|| sudo halt