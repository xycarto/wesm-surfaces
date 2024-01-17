import os
import boto3
import geopandas as gp
import subprocess as sub
from osgeo import gdal
import sys
sys.path.append('pyutils')
from general import *
import rasterio as rio
import shutil


def main():
    
    s3 = get_creds()
    
    get_s3_file(s3, IN_FILE, WESM_BUCKET)  

    rio_in_file = rio.open(IN_FILE)
    crs = rio_in_file.crs
    bounds = rio_in_file.bounds

    print(bounds)
         
    for day in DAYS:     
        print(day)    
        sub.call(f"bash process/solar/grass-build.sh {IN_FILE} {day} {crs} {SOLAR_DIR_TMP}", shell=True) 

    tmp_tif_list = [f"{SOLAR_DIR_TMP}/{tif}" for tif in os.listdir(SOLAR_DIR_TMP)]
        
    print("Creating Average...")
    tif_avg = f"{SOLAR_DIR}/{os.path.basename(IN_FILE)}"
    sub.call(
        f"gdal_calc.py \
        --overwrite \
        -A {tmp_tif_list[0]} \
        -B {tmp_tif_list[1]} \
        -C {tmp_tif_list[2]} \
        -D {tmp_tif_list[3]} \
        --outfile={tif_avg} \
        --NoDataValue=0 \
        --projwin {bounds[0]} {bounds[3]} {bounds[2]} {bounds[1]} \
        --calc '(A + B + C + D)/4'", 
        shell=True
        )
    
    shutil.rmtree(SOLAR_DIR_TMP)
        
    # s3.upload_file(tif_avg, WESM_BUCKET, tif_avg)
        
if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]
    WESM_BUCKET = "xyc-wesm-surfaces"
    DATA_DIR = "data"
    DSM_DIR = f"{DATA_DIR}/dsm/{STATE}/{WORKUNIT}"
    SOLAR_DIR = f"{DATA_DIR}/solar/{STATE}/{WORKUNIT}"
    SOLAR_DIR_TMP = f"{DATA_DIR}/solar/{STATE}/{WORKUNIT}/{os.path.basename(IN_FILE).split('.')[0]}"

    DAYS = [80, 173, 266, 355]
    # DAYS = [80]

    for d in [DATA_DIR, DSM_DIR, SOLAR_DIR, SOLAR_DIR_TMP]:
        os.makedirs(d, exist_ok=True)
    
    main()