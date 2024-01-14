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
        
    dsm_file_tmp = f"{DSM_DIR}/{BASENAME}-tmp.tif"
    dsm_file_clip = f"{DSM_DIR}/{BASENAME}.tif"   

    metadata = get_pc_metadata(IN_FILE)    

    make_surface(PIPELINE_PATH, IN_FILE, metadata.wkt, dsm_file_tmp, metadata.bounds)
    
    tmp_gpkg, out_tif = gdal_clip(BASENAME, IN_FILE, INDEX_FILE, dsm_file_tmp, dsm_file_clip)
    
    print("Creating DSM...")
    
    print(f"Uploading {out_tif}...")
    s3.upload_file(out_tif, WESM_BUCKET, out_tif)

    os.remove(tmp_gpkg)
    os.remove(dsm_file_tmp)

if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]
    WESM_BUCKET = "xyc-wesm-surfaces"
    DATA_DIR = "data"
    BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}" 
    DSM_DIR = f"{DATA_DIR}/dsm/{STATE}/{WORKUNIT}"
    PIPELINE_PATH = 'process/pipeline-templates/dsm_template.json'
    INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
    INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"

    for d in [DATA_DIR, BCM_DIR, DSM_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()