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

    repro_file = os.path.join(REPRO_DIR, os.path.basename(IN_FILE))
    gdal.Warp(
        repro_file,
        IN_FILE,
        dstSRS='EPSG:3857'
    ) 
    
    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)


if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    IN_DIR = sys.argv[2]
    WORKUNIT = sys.argv[3]
    STATE = sys.argv[4]
    DATA_DIR = "data"
    COG_DIR = os.path.join(DATA_DIR, "cog", STATE, WORKUNIT)
    REPRO_DIR = os.path.join(COG_DIR, "repro", IN_DIR)
    WESM_BUCKET = "wesm"

    for d in [DATA_DIR, COG_DIR, REPRO_DIR]:
        os.makedirs(d, exist_ok=True)

    main()