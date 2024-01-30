#!/usr/bin/env python
import os
import boto3
import sys
import subprocess as sub
from osgeo import gdal
from py_utils import *
from globals import *


def main():
    s3 = get_creds()    

    out_hs = f"{SLOPE_DIR}/{BASENAME}"  
    gdal.DEMProcessing(
        out_hs,
        f"{DIR_PATH}/{BASENAME}",
        'slope',
        computeEdges=True,
        callback=gdal.TermProgress_nocb,
    )

if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    BASENAME = f"{os.path.basename(IN_FILE).split('.')[0]}.tif"
    DIR_PATH = os.path.dirname(IN_FILE)
    SLOPE_DIR = f"{DIR_PATH}/slope"

    for d in [DATA_DIR, SLOPE_DIR]:
        os.makedirs(d, exist_ok=True)

    main()