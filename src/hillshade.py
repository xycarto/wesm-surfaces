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

    get_s3_file(s3, f"{DIR_PATH}/{BASENAME}", WESM_SURFACE_BUCKET)

    out_hs = f"{HS_DIR}/{BASENAME}"  
    gdal.DEMProcessing(
        out_hs,
        f"{DIR_PATH}/{BASENAME}",
        'hillshade',
        computeEdges=True,
        callback=gdal.TermProgress_nocb,
    )

if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    BASENAME = f"{os.path.basename(IN_FILE).split('.')[0]}.tif"
    DIR_PATH = os.path.dirname(IN_FILE)
    HS_DIR = f"{DIR_PATH}/hillshade"

    for d in [DATA_DIR, HS_DIR]:
        os.makedirs(d, exist_ok=True)

    main()