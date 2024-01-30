import os
import boto3
import geopandas as gp
import subprocess as sub
from osgeo import gdal
import sys
sys.path.append('src')
from py_utils import *
from globals import *
import rasterio as rio
import shutil


def main():
    
    in_file = f"{DIR_PATH}/{BASENAME}"

    s3 = get_creds()
    
    get_s3_file(s3, in_file, WESM_SURFACE_BUCKET)  

    rio_in_file = rio.open(in_file)
    crs = rio_in_file.crs
    bounds = rio_in_file.bounds
         
    for day in DAYS:     
        print(day)    
        sub.call(f"bash src/solar/grass-build.sh {in_file} {day} {crs} {SOLAR_DIR_TMP}", shell=True) 

    tmp_tif_list = [f"{SOLAR_DIR_TMP}/{tif}" for tif in os.listdir(SOLAR_DIR_TMP)]
        
    print("Creating Average...")
    tif_avg = f"{SOLAR_DIR}/{BASENAME}"
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
        
if __name__ == "__main__":
    IN_FILE = sys.argv[1]    
    BASENAME = f"{os.path.basename(IN_FILE).split('.')[0]}.tif"
    DIR_PATH = os.path.dirname(IN_FILE)
    SOLAR_DIR_TMP = f"{DATA_DIR}/solar/{STATE}/{WORKUNIT}/{os.path.basename(IN_FILE).split('.')[0]}"   

    DAYS = [80, 173, 266, 355]
    # DAYS = [80]

    for d in [DATA_DIR, DSM_DIR, SOLAR_DIR, SOLAR_DIR_TMP]:
        os.makedirs(d, exist_ok=True)
    
    main()