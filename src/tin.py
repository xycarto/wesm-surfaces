#!/usr/bin/env python
import os
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
from py_utils import *
from globals import *


def main():
    s3 = get_creds()    
    get_s3_file(s3, IN_FILE, WESM_SURFACE_BUCKET)

    tin_file_tmp = f"{TIN_DIR}/{BASENAME}-tmp.tif"
    tin_file_clip = f"{TIN_DIR}/{BASENAME}.tif"

    metadata = get_pc_metadata(IN_FILE)    

    print("Creating TIN...")
    
    make_surface(PIPELINE_TIN, IN_FILE, metadata.wkt, tin_file_tmp, metadata.bounds)

    tmp_gpkg, out_tif = gdal_clip(DATA_DIR, BASENAME, IN_FILE, INDEX_FILE, tin_file_tmp, tin_file_clip)
    
    print(f"Uploading {out_tif}...")
    s3.upload_file(out_tif, WESM_SURFACE_BUCKET, out_tif)

    os.remove(tmp_gpkg)
    os.remove(tin_file_tmp)
    
if __name__ == "__main__":

    IN_FILE = sys.argv[1]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]
    
    for d in [DATA_DIR, BCM_DIR, TIN_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()