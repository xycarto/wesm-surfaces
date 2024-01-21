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

    repro_file = os.path.join(REPRO_DIR, os.path.basename(IN_FILE))
    if PROCESS == 'solar':
        print("Making Solar Repro for COG...")
        gdal.Warp(
            repro_file,
            IN_FILE,
            outputType=gdal.GDT_UInt16,
            dstSRS='EPSG:3857',
        ) 
    else:
        gdal.Warp(
            repro_file,
            IN_FILE,
            dstSRS='EPSG:3857',
        ) 
    
    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)


if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    if HS == "true":
        REPRO_DIR = f"{COG_DIR}/repro/{PROCESS}/hillshade"
    else:
        REPRO_DIR = f"{COG_DIR}/repro/{PROCESS}"

    for d in [DATA_DIR, COG_DIR, REPRO_DIR]:
        os.makedirs(d, exist_ok=True)

    main()