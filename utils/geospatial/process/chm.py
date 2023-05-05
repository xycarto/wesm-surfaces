#!/usr/bin/env python
import os
import boto3
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import json

# python3 process/chm.py path/to/laz.laz


def main():
    s3 = get_creds()
    
    dsm_file, dem_file = get_files(s3)
    chm_file = process_chm(dsm_file, dem_file)

    print(f"Uploading {chm_file}...")
    s3.upload_file(chm_file, BUCKET, chm_file)
        
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

def get_files(s3):
    # Get Data for Download, download, process
    dsm_file = f"{DSM_PATH}/{os.path.basename(IN_FILE).split('.')[0]}.tif"
    dem_file = f"{DEM_PATH}/{os.path.basename(IN_FILE).split('.')[0]}.tif"

    for f in [dsm_file, dem_file]:
        if not os.path.exists(f):
            print(f"Downloading: {f}...")
            s3.download_file(BUCKET, f, f, ExtraArgs={'RequestPayer':'requester'})
            
    return dsm_file, dem_file

def process_chm(dsm_file, dem_file):
    chm_file = f"{CHM_PATH}/{os.path.basename(IN_FILE).split('.')[0]}.tif"
    tmp_chm = f"{CHM_PATH}/{os.path.basename(IN_FILE).split('.')[0]}_tmp.tif"
    
    sub.call(     
    f"""gdal_calc.py --overwrite --calc="A-B" -A {dsm_file} -B {dem_file} --outfile={tmp_chm}""",
    shell=True
    )

    sub.call(     
    f"""gdal_calc.py --overwrite --calc="A*(A>0)" -A {tmp_chm} --NoDataValue=-9999 --outfile={chm_file}""",
    shell=True
    )
    
    os.remove(tmp_chm)
    
    return chm_file
        
if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT =IN_FILE.split('/')[-2]
    BUCKET = os.environ.get("AWS_BUCKET")
    LAZ_PATH = f"data/laz/{WORKUNIT}"
    DEM_PATH = f"data/dem/{WORKUNIT}"
    DSM_PATH = f"data/dsm/{WORKUNIT}"
    CHM_PATH = f"data/chm/{WORKUNIT}"

    os.makedirs(LAZ_PATH, exist_ok=True)
    os.makedirs(DEM_PATH, exist_ok=True)
    os.makedirs(DSM_PATH, exist_ok=True)
    os.makedirs(CHM_PATH, exist_ok=True)
    
    main()