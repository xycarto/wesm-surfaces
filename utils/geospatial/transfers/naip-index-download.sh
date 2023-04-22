#!/bin/bash

## Example of downloading NAIP index file
aws s3 cp --recursive --request-payer requester s3://naip-analytic/nv/2019/60cm/index ./data/naip-index-nv --profile vpTemp