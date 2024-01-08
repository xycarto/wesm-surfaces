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


def main():
    s3 = get_creds()    
    get_s3_file(s3, IN_FILE, WESM_BUCKET)
        
    metadata = get_pc_metadata(IN_FILE)    
    
    print("Creating DSM...")
    dsm_file = f"{DSM_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.tif"
    make_surface(PIPELINE_PATH, IN_FILE, metadata.wkt, dsm_file, metadata.bounds)
    

    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)


if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    WESM_BUCKET = "wesm"
    DATA_DIR = "data"
    BCM_DIR = os.path.join(DATA_DIR, "bcm", STATE, WORKUNIT)  
    DSM_DIR = os.path.join(DATA_DIR, "dsm", STATE, WORKUNIT)
    PIPELINE_PATH = 'process/pipeline-templates/dsm_template.json'

    for d in [DATA_DIR, BCM_DIR, DSM_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()