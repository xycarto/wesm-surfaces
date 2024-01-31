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

    if 'hillshade' in IN_DIR:
        repro_dir = f"{COG_DIR}/repro/{IN_DIR.split('/')[1]}/hillshade"
    else:
        repro_dir = f"{COG_DIR}/repro/{IN_DIR.split('/')[1]}"

    if 'hillshade' in repro_dir:
        file_name = f"{IN_DIR.split('/')[1]}-hs"
    else:
        file_name = f"{IN_DIR.split('/')[1]}"

    tifs = [f"{os.path.join(repro_dir, tif)}" for tif in os.listdir(repro_dir) if not os.path.isdir(tif) and tif.endswith('.tif')]

    vrt = f"{repro_dir}{file_name}.vrt"
    gdal.BuildVRT(
        vrt,
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
        f"{COG_DIR}/{file_name}-cog.tif",
        vrt,
        format = "COG",
        callback=gdal.TermProgress_nocb,
        creationOptions = creation_options
    )

if __name__ == "__main__":
    IN_DIR = sys.argv[1]

    for d in [DATA_DIR, COG_DIR]:
        os.makedirs(d, exist_ok=True)

    main()