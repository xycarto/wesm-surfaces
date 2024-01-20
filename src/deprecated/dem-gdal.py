#!/usr/bin/env python
import os
import boto3
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import json
sys.path.append('pyutils')
from general import *
from osgeo import gdal


def main():
    s3 = get_creds()    
    get_s3_file(s3, IN_FILE, WESM_BUCKET)
        
    proj4, bounds = get_pc_metadata(IN_FILE)   
    
    print("Creating Points...")
    gpkg_file = f"{DEM_POINTS_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.gpkg"
    make_points(PIPELINE_PATH, IN_FILE, proj4, gpkg_file)

    print("GDAL Linear Interpolation...")
    gdal_file = f"{DEM_GDAL_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.tif"
    minx, miny, maxx, maxy = get_bound_info(IN_FILE)
    gdal.Grid(
        gdal_file,
        gpkg_file,
        algorithm="linear:radius=10.0:nodata=0.0",
        outputBounds=[minx,maxy,maxx,miny]
    )

    # sub.call(f"gdal_grid -l points -a linear:radius=100.0:nodata=0.0 -ot Float32 -of GTiff {gpkg_file} {gdal_file}", shell=True)
    
    # print(f"Uploading {dsm_file}...")
    # s3.upload_file(dsm_file, BUCKET, dsm_file)

def make_points(pipeline, in_pc, proj4, out_gpkg):
    sub.call(
        f"pdal pipeline '{pipeline}' \
            --readers.las.filename='{in_pc}' \
            --readers.las.spatialreference='{proj4}' \
            --writers.ogr.filename='{out_gpkg}'",
        shell=True,
    )

if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    WESM_BUCKET = "wesm"
    DATA_DIR = "data"
    BCM_DIR = os.path.join(DATA_DIR, "bcm", STATE, WORKUNIT)  
    DEM_POINTS_DIR = os.path.join(DATA_DIR, "dem-points", STATE, WORKUNIT)
    DEM_GDAL_DIR = os.path.join(DATA_DIR, "dem-gdal", STATE, WORKUNIT)
    PIPELINE_PATH = 'process/pipeline-templates/dem_gdal_template.json'

    for d in [DATA_DIR, BCM_DIR, DEM_POINTS_DIR, DEM_GDAL_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()