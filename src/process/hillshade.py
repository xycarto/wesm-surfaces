#!/usr/bin/env python
import os
import boto3
import sys
import subprocess as sub
from osgeo import gdal
sys.path.append('pyutils')
from general import *


def main():
    s3 = get_creds()    

    out_hs = os.path.join(HS_DIR, os.path.basename(IN_FILE))  
    sub.call(
        f"gdaldem hillshade {IN_FILE} {out_hs}",
        shell=True
    )
    
    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)


if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    IN_DIR = sys.argv[2]
    WORKUNIT = sys.argv[3]
    STATE = sys.argv[4]
    DATA_DIR = "data"
    SURFACE_DIR = f"{DATA_DIR}/{IN_DIR}/{STATE}/{WORKUNIT}"
    HS_DIR = f"{SURFACE_DIR}/hillshade"
    WESM_SURFACE_BUCKET = "xyc-wesm-surfaces"

    for d in [DATA_DIR, SURFACE_DIR, HS_DIR]:
        os.makedirs(d, exist_ok=True)

    main()