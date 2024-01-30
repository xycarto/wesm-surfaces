#!/usr/bin/env python
import os
import boto3
import geopandas as gp
import subprocess as sub
import sys
from py_utils import *
from globals import *

def main():
    s3 = get_creds()
    
    dsm_file, dem_file = get_chm_files(s3)
    process_chm(dsm_file, dem_file)

def get_chm_files(s3):
    # Get Data for Download, download, process
    dsm_file = f"{DSM_DIR}/{BASENAME}.tif"
    dem_file = f"{DEM_DIR}/{BASENAME}.tif"

    for f in [dsm_file, dem_file]:
        if not os.path.exists(f):
            print(f"Downloading: {f}...")
            s3.download_file(WESM_SURFACE_BUCKET, f, f, ExtraArgs={'RequestPayer':'requester'})
            
    return dsm_file, dem_file

def process_chm(dsm_file, dem_file):
    chm_file = f"{CHM_DIR}/{BASENAME}.tif"
    tmp_chm = f"{CHM_DIR}/{BASENAME}_tmp.tif"
    
    sub.call(     
        f"""gdal_calc.py \
            --overwrite \
            --calc="A-B" \
            -A {dsm_file} \
            -B {dem_file} \
            --outfile={tmp_chm}""",
        shell=True
    )

    sub.call(     
        f"""gdal_calc.py \
            --overwrite \
            --calc="A*(A>0)" \
            -A {tmp_chm} \
            --NoDataValue=-9999 \
            --outfile={chm_file}""",
        shell=True
    )
    
    os.remove(tmp_chm)
        
if __name__ == "__main__":

    IN_FILE = sys.argv[1]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]
    
    for d in [DSM_DIR, DEM_DIR, CHM_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()