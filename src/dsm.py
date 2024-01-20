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
        
    dsm_file_tmp = f"{DSM_DIR}/{BASENAME}-tmp.tif"
    dsm_file_clip = f"{DSM_DIR}/{BASENAME}.tif"   

    metadata = get_pc_metadata(IN_FILE)    

    make_surface(PIPELINE_DSM, IN_FILE, metadata.wkt, dsm_file_tmp, metadata.bounds)
    
    tmp_gpkg, out_tif = gdal_clip(DATA_DIR, BASENAME, IN_FILE, INDEX_FILE, dsm_file_tmp, dsm_file_clip)    
     
    print(f"Uploading {out_tif}...")
    s3.upload_file(out_tif, WESM_SURFACE_BUCKET, out_tif)

    os.remove(tmp_gpkg)
    os.remove(dsm_file_tmp)

if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]

    for d in [DATA_DIR, BCM_DIR, DSM_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()