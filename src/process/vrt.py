#!/usr/bin/env python
import os
import boto3
import sys
from osgeo import gdal
sys.path.append('pyutils')
from general import *


def main():
    s3 = get_creds()    
    
    if os.path.basename(IN_DIR) == "hillshade":
        vrt_dir = os.path.join(VRT_DIR, "hillshade")
        in_dir = IN_DIR.split("/")[0]
        vrt = os.path.join(vrt_dir, f"{in_dir}-hillshade.vrt")
        build_vrt(vrt_dir, vrt)
    else:
        vrt = os.path.join(VRT_DIR, f"{IN_DIR}.vrt")
        build_vrt(VRT_DIR, vrt)
     
        

    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)


if __name__ == "__main__":
    IN_DIR = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    DATA_DIR = "data"
    VRT_DIR = os.path.join(DATA_DIR, IN_DIR.split("/")[0], STATE, WORKUNIT)
    WESM_BUCKET = "wesm"

    for d in [DATA_DIR]:
        os.makedirs(d, exist_ok=True)

    main()