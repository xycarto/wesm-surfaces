#!/usr/bin/env python
import os
import boto3
import sys
import subprocess as sub
from osgeo import gdal
sys.path.append('pyutils')
from general import *


def main():
    s3 = get_creds()   

    vrt = f"{REPRO_DIR}/{'-'.join(IN_DIR.split('/'))}-repro.vrt"
    tifs = [f"{os.path.join(REPRO_DIR, tif)}" for tif in os.listdir(REPRO_DIR) if not os.path.isdir(tif) and tif.endswith('.tif')]
    
    gdal.BuildVRT(
        vrt,
        tifs,
        resolution='average'
    ) 

    cog_file = f"{COG_DIR}/{'-'.join(IN_DIR.split('/'))}-cog.tif"

    # Make Python process in future
    sub.call(
        f"gdal_translate {vrt} {cog_file} -of COG -co TILING_SCHEME=GoogleMapsCompatible -co COMPRESS=LZW -co BIGTIFF=YES -co NUM_THREADS=ALL_CPUS",
        shell=True
    )

    print(f"Uploading {cog_file}...")
    s3.upload_file(cog_file, WESM_VIEWER_BUCKET, cog_file, ExtraArgs={'ACL': 'public-read'})


if __name__ == "__main__":
    IN_DIR = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    DATA_DIR = "data"
    COG_DIR = f"{DATA_DIR}/cog/{STATE}/{WORKUNIT}"
    REPRO_DIR = f"{COG_DIR}/repro/{IN_DIR}"
    WESM_BUCKET = "xyc-wesm-surfaces"
    WESM_VIEWER_BUCKET = "xyc-wesm-viewer"

    for d in [DATA_DIR, COG_DIR, REPRO_DIR]:
        os.makedirs(d, exist_ok=True)

    main()