#!/usr/bin/env python
import os
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import rasterio as rio
import sys
sys.path.append('src')
from py_utils import *
from globals import *


def main():
    s3 = get_creds()    
    get_s3_file(s3, IN_FILE, WESM_SURFACE_BUCKET)

    # tin_file_tmp = f"{TIN_DIR}/{BASENAME}-tmp.tif"
    tin_file = f"{TIN_DIR}/{BASENAME}.tif"
    bcm_file = f"{BCM_DIR}/{BASENAME}.laz"

    print("Getting Bounds...")    
    pc_bounds= get_bound_info(bcm_file)  
    tiff_bounds = gtiff_bounds(tin_file)

    print('Testing Bounds...')
    if pc_bounds == tiff_bounds:
        print("bounds match")

def gtiff_bounds(tin_file):
    rio_gtiff = rio.open(tin_file)
    bounds = rio_gtiff.bounds
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]

    return int(minx), int(miny), int(maxx), int(maxy)

if __name__ == "__main__":

    IN_FILE = sys.argv[1]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]
    
    for d in [DATA_DIR, BCM_DIR, TIN_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()