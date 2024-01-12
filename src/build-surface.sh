#!/bin/bash

source .creds

WORKUNIT=$1
STATE=$2

git clone https://${TOKEN}@github.com/xycarto/wesm-surfaces.git

cp -r .creds wesm-surfaces/src/

cd wesm-surfaces/src && \
    make docker-pull && \
    echo $WORKUNIT && \
    echo $STATE

exit