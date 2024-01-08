#!/usr/bin/env python
import os
import boto3
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import json
sys.path.append('pyutils')
from general import *
from osgeo import gdal


def main():
    s3 = get_creds()    
    get_s3_file(s3, IN_FILE, WESM_BUCKET)
        
    proj4, bounds = get_pc_metadata(IN_FILE)   
    
    print("Creating Points...")
    gpkg_file = f"{HEXBIN_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.gpkg"
    make_hexbin(PIPELINE_PATH, IN_FILE, proj4, gpkg_file)

    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)

# def make_hexbin(pipeline, in_pc, proj4, json_file):
#     sub.call(
#         f"pdal pipeline '{pipeline}' \
#             --readers.las.filename='{in_pc}' \
#             --readers.las.spatialreference='{proj4}' \
#             --boundary {json_file}",
#         shell=True,
#     )

def make_hexbin(pipeline, in_pc, proj4, gpkg_file):
    sub.call(
        f"pdal density \
            --output {gpkg_file} \
            --input {IN_FILE} \
            -f GPKG",
            shell=True
    )



if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    WESM_BUCKET = "wesm"
    DATA_DIR = "data"
    BCM_DIR = os.path.join(DATA_DIR, "bcm", STATE, WORKUNIT)  
    HEXBIN_DIR = os.path.join(DATA_DIR, "hexbin", STATE, WORKUNIT)
    PIPELINE_PATH = 'process/pipeline-templates/hexbin_template.json'

    for d in [DATA_DIR, BCM_DIR, HEXBIN_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()