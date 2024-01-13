#!/usr/bin/env python
import os
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import shutil
sys.path.append('pyutils')
from general import *

def main():
    s3 = get_creds()
    get_s3_file(s3, INDEX_FILE, WESM_BUCKET)
    

    pc_file = os.path.join(PC_DIR, os.path.basename(IN_FILE))

    # Buffer Index
    index_file = gp.read_file(INDEX_FILE)
    index_row = index_file[index_file['file_name'] == os.path.basename(IN_FILE)]

    filter_laz(pc_file, index_row)

    # print(clipped_array)
    
             
    # print(f"Uploading... {bcm_file}")   
    # s3.upload_file(bcm_file, WESM_BUCKET, bcm_file)

    # shutil.rmtree(CLIP_DIR)

    # os.remove(bcm_file)


def filter_laz(merged_pc, index_row):
    print("Filtering...")   
    bcm_file =  f"{BCM_DIR}/{os.path.basename(IN_FILE)}"
    crs = f"EPSG:{index_row.native_horiz_crs.values[0]}"
    sub.call(
        f"pdal -v 0 pipeline '{PIPELINE_FILTER}' \
            --readers.las.filename='{merged_pc}' \
            --writers.las.filename='{bcm_file}' \
            --writers.las.a_srs='{crs}'",
        shell=True,
    )
   
if __name__ == "__main__":

    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    WESM_BUCKET = "xyc-wesm-surfaces"
    DATA_DIR = "data"
    PC_DIR = f"{DATA_DIR}/point-clouds/{STATE}/{WORKUNIT}"
    BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}"       
    CLIP_DIR = f"{DATA_DIR}/clips/{os.path.basename(IN_FILE).split('.')[0]}"
    INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
    INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"
    BUFFER = 50
    PIPELINE_FILTER = 'process/pipeline-templates/buffer-clip-filter-template-filter-only.json'

    
    for d in [DATA_DIR, PC_DIR, BCM_DIR, CLIP_DIR, INDEX_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()