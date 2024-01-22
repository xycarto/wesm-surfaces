#!/usr/bin/env python
import os
import boto3
import sys
import subprocess as sub
from osgeo import gdal
from py_utils import *
from globals import *


def main():
    s3 = get_creds()   

    tifs = [f"{os.path.join(REPRO_DIR, tif)}" for tif in os.listdir(REPRO_DIR) if not os.path.isdir(tif) and tif.endswith('.tif')]
    
    gdal.BuildVRT(
        VRT,
        tifs,
    ) 

    creation_options = [
    "COMPRESS=DEFLATE",
    "BIGTIFF=YES",
    "NUM_THREADS=ALL_CPUS",
    "OVERVIEW_RESAMPLING=LANCZOS",
    "WARP_RESAMPLING=BILINEAR",
    "OVERVIEW_COMPRESS=DEFLATE",
    ]

    gdal.Translate(    
        COG_FILE,
        VRT,
        format = "COG",
        callback=gdal.TermProgress_nocb,
        creationOptions = creation_options
    )

    print(f"Uploading {COG_FILE}...")
    s3.upload_file(COG_FILE, WESM_SURFACE_BUCKET, COG_FILE, ) # ExtraArgs={'ACL': 'public-read'}


if __name__ == "__main__":
    if HS == "true" and PROCESS != "solar":
        REPRO_DIR = f"{COG_DIR}/repro/{PROCESS}/hillshade"
        VRT = f"{REPRO_DIR}/{PROCESS}-hillshade-repro.vrt"
        COG_FILE = f"{COG_DIR}/{PROCESS}-hillshade-cog.tif"
    else:
        REPRO_DIR = f"{COG_DIR}/repro/{PROCESS}"
        VRT = f"{REPRO_DIR}/{PROCESS}-repro.vrt"
        COG_FILE = f"{COG_DIR}/{PROCESS}-cog.tif"

    for d in [DATA_DIR, COG_DIR, REPRO_DIR]:
        os.makedirs(d, exist_ok=True)

    main()