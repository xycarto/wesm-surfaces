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
     
        
    print(f"Uploading {vrt}...")
    # s3.upload_file(vrt, WESM_SURFACE_BUCKET, vrt)


if __name__ == "__main__":
    IN_DIR = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    TYPE = sys.argv[4]
    if TYPE == "test":
        DATA_DIR = "test-data"    
    else:
        DATA_DIR = "data"
    VRT_DIR = f"{DATA_DIR}/{IN_DIR.split('/')[0]}/{STATE}/{WORKUNIT}"
    WESM_SURFACE_BUCKET = "xyc-wesm-surfaces"

    for d in [DATA_DIR]:
        os.makedirs(d, exist_ok=True)

    main()