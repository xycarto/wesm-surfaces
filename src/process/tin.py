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
    get_s3_file(s3, INDEX_FILE, WESM_BUCKET)

    metadata = get_pc_metadata(IN_FILE)    
    
    print("Creating TIN...")
    tin_file_tmp = f"{TIN_DIR}/{BASENAME}-tmp.tif"
    tin_file_clip = f"{TIN_DIR}/{BASENAME}.tif"
    make_tin(PIPELINE_PATH, IN_FILE, metadata, tin_file_tmp)

    tmp_gpkg, out_tif = gdal_clip(BASENAME, IN_FILE, INDEX_FILE, tin_file_tmp, tin_file_clip)
    
    print(f"Uploading {out_tif}...")
    s3.upload_file(out_tif, WESM_BUCKET, out_tif)

    os.remove(tmp_gpkg)
    os.remove(tin_file_tmp)
    
def make_tin(pipeline, in_pc, metadata, out_tif):
    sub.call(
        f"pdal pipeline '{pipeline}' \
            --readers.las.filename='{in_pc}' \
            --readers.las.spatialreference='{metadata.wkt}' \
            --writers.gdal.filename='{out_tif}' \
            --writers.gdal.bounds={metadata.bounds}",
            shell=True,
    )
    


if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]
    WESM_BUCKET = "xyc-wesm-surfaces"
    DATA_DIR = "data"
    BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}"  
    TIN_DIR = f"{DATA_DIR}/tin/{STATE}/{WORKUNIT}"
    PIPELINE_PATH = 'process/pipeline-templates/tin_template.json'
    INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
    INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"

    for d in [DATA_DIR, BCM_DIR, TIN_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()