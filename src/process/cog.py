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

    vrt = os.path.join(REPRO_DIR, f"{IN_DIR}-repro.vrt")
    tifs = [f"{os.path.join(REPRO_DIR, tif)}" for tif in os.listdir(REPRO_DIR) if not os.path.isdir(tif) and tif.endswith('.tif')]

    gdal.BuildVRT(
        vrt,
        tifs,
        resolution='average'
    ) 

    cog_file = os.path.join(COG_DIR, f"{IN_DIR}-cog.tif")
    # Make Python process in future
    sub.call(
        f"gdal_translate {vrt} {cog_file} -of COG -co TILING_SCHEME=GoogleMapsCompatible -co COMPRESS=LZW -co BIGTIFF=YES",
        shell=True
    )

    # if os.path.basename(IN_DIR) == "hillshade":
    #     vrt_dir = os.path.join(VRT_DIR, "hillshade")
    #     in_dir = IN_DIR.split("/")[0]
    #     tifs = [f"{os.path.join(vrt_dir, tif)}" for tif in os.listdir(vrt_dir) if not os.path.isdir(tif) and tif.endswith('.tif')]
    #     # build_vrt(vrt_dir, vrt)
    # else:
    #     vrt = os.path.join(VRT_DIR, f"{IN_DIR}.vrt")
    #     # build_vrt(VRT_DIR, vrt)
     
        

    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)


if __name__ == "__main__":
    IN_DIR = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    DATA_DIR = "data"
    COG_DIR = os.path.join(DATA_DIR, "cog", STATE, WORKUNIT)
    REPRO_DIR = os.path.join(COG_DIR, "repro", IN_DIR)
    WESM_BUCKET = "wesm"

    for d in [DATA_DIR, COG_DIR, REPRO_DIR]:
        os.makedirs(d, exist_ok=True)

    main()