import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gp
import boto3
import sys
import subprocess as sub
import re
from shapely.geometry import Polygon
import shutil
import laspy
sys.path.append('pyutils')
from general import *

# python3 process/make-vector-tiles-hexbin.py CA_NoCAL_Wildfires_B1_2018 California

def main():    
    s3 = get_creds()
        
    # Download WESM
    print("Get GPKG...")
    get_s3_file(s3, IN_FILE, WESM_SURFACE_BUCKET)

    print("Make Geopandas...")
    in_file = gp.read_file(IN_FILE)
    # repro_out = f"{HEXBIN_DIR}/{WORKUNIT}-hexbin-merged-3857.gpkg"
    # print("repro")
    # repro = in_file.to_crs(3857).to_file(repro_out, driver="GPKG")


    # print("Making Vector Tiles...")
    # shutil.rmtree(VTILES_DIR)
    # sub.call(
    #     f"ogr2ogr -f MVT {VTILES_DIR} {repro_out} -dsco MINZOOM=0 -dsco MAXZOOM=16 -dsco COMPRESS=NO ",
    #     shell=True
    # )    
    
    # print(f"Uploading... {VTILES_DIR}")   
    # sub.call(
    #     f"aws s3 cp --recursive {VTILES_DIR} s3://{WESM_VIEWER_BUCKET}/{VTILES_DIR} --acl public-read",
    #     shell=True
    # ) 
   

if __name__ == "__main__":
    
    WESM_SURFACE_BUCKET="xyc-wesm-surfaces"
    WESM_VIEWER_BUCKET="xyc-wesm-viewer"
    WORKUNIT = sys.argv[1]
    STATE = sys.argv[2]
    DATA = "data"
    HEXBIN_DIR = f"{DATA}/hexbin/{STATE}/{WORKUNIT}"
    VTILES_DIR = f"{DATA}/vector-tiles/hexbin/{STATE}/{WORKUNIT}"
    IN_FILE = f"{HEXBIN_DIR}/{WORKUNIT}-hexbin-merged.gpkg"
    
    for d in [DATA, HEXBIN_DIR, VTILES_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()