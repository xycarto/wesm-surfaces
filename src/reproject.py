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

    in_file = f"{DIR_PATH}/{BASENAME}"

    if 'hillshade' in DIR_PATH:
        repro_dir = f"{COG_DIR}/repro/{DIR_PATH.split('/')[1]}/hillshade"
    else:
        repro_dir = f"{COG_DIR}/repro/{DIR_PATH.split('/')[1]}"

    
    print(repro_dir)
    os.makedirs(repro_dir, exist_ok=True)

    repro_file = f"{repro_dir}/{BASENAME}"
    if 'solar' in repro_dir:
        print("Making Solar Repro for COG...")
        gdal.Warp(
            repro_file,
            in_file,
            outputType=gdal.GDT_UInt16,
            dstSRS='EPSG:3857',
        ) 
    else:
        gdal.Warp(
            repro_file,
            in_file,
            dstSRS='EPSG:3857',
        ) 
    
if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    BASENAME = f"{os.path.basename(IN_FILE).split('.')[0]}.tif"
    DIR_PATH = os.path.dirname(IN_FILE)

    for d in [DATA_DIR, COG_DIR,]:
        os.makedirs(d, exist_ok=True)

    main()