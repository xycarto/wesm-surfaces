#!/usr/bin/env python
import os
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import shutil
from py_utils import *
from globals import *


def main():
    s3 = get_creds()
    get_grid_index(s3, WESM_GRID_BUCKET, GRID_INDEX_FILE, INDEX_FILE)

    index_file = gp.read_file(INDEX_FILE)
    index_row = index_file[index_file['file_name'] == os.path.basename(IN_FILE)]

    filter_laz(IN_FILE, index_row)
    

def filter_laz(in_file, index_row):
    print("Filtering...")   
    bcm_file =  f"{BCM_DIR}/{os.path.basename(in_file)}"
    crs = f"EPSG:{index_row.native_horiz_crs.values[0]}"
    sub.call(
        f"pdal -v 0 --nostream pipeline '{PIPELINE_FILTER}' \
            --readers.las.filename='{in_file}' \
            --writers.las.filename='{bcm_file}' \
            --writers.las.a_srs='{crs}'",
        shell=True,
    )

def merge_pc(clipped_array):       
    print("Merging...")
    merged_pc = f"{BCM_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.laz"
    sub.call(
        f"""pdal -v 0 merge {" ".join(clipped_array)} {merged_pc}""",
        shell=True,
    )
    return merged_pc

       
if __name__ == "__main__":

    IN_FILE = sys.argv[1]
    CLIP_DIR = f"{DATA_DIR}/clips/{os.path.basename(IN_FILE).split('.')[0]}"
        
    for d in [DATA_DIR, PC_DIR, BCM_DIR,INDEX_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()