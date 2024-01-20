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

    index_file = gp.read_file(INDEX_FILE)
    index_row = index_file[index_file['file_name'] == os.path.basename(IN_FILE)]    
    index_repro = index_file.to_crs(index_row.native_horiz_crs.values[0])
    index_repro_row = index_repro[index_repro['file_name'] == os.path.basename(IN_FILE)]


    print("Clipping BCM...")
    clipped_laz = clip_files(index_repro_row)    
    gpkg_file = f"{HEXBIN_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.gpkg"

    sub.call(
        f"pdal pipeline process/pipeline-templates/hexbin_template.json \
            --readers.las.filename='{IN_FILE}' \
            --writers.ogr.filename='{gpkg_file}'", shell=True
    )
    # metadata = get_pc_metadata(IN_FILE)   
    
    # print("Creating Points...")
    # gpkg_file_tmp = f"{HEXBIN_DIR_TMP}/{os.path.basename(IN_FILE).split('.')[0]}-tmp.gpkg"
    # gpkg_file = f"{HEXBIN_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.gpkg"
    # make_hexbin(clipped_laz, gpkg_file_tmp)

    # print("Make Single...")
    # tmp_gpkg = gp.read_file(gpkg_file_tmp).explode
    # tmp_gpkg.to_file(gpkg_file, driver="GPKG")

    # # print("Making Multi")
    # # sub.call(
    # #     f"ogr2ogr -overwrite -nlt PROMOTE_TO_MULTI  {gpkg_file} {gpkg_file_tmp}",
    # #     shell=True
    # # )

    # # print(f"Uploading {dsm_file}...")
    # # s3.upload_file(dsm_file, BUCKET, dsm_file)

def make_hexbin(clipped_laz, gpkg_file):
    sub.call(
        f"pdal density \
            --output {gpkg_file} \
            --input {clipped_laz} \
            -f GPKG",
            shell=True
    )

def clip_files(index_repro_row):
    print(f"Clipping Input Point Cloud...")
    clipped_laz = f"{CLIP_DIR}/{os.path.basename(IN_FILE).split('.')[0]}_tmp_crop.laz"
    sub.call(
        f"pdal -v 0 pipeline '{PIPELINE_CROP_PATH}' \
            --readers.las.filename='{IN_FILE}' \
            --filters.crop.polygon='{index_repro_row.geometry.values[0]}' \
            --writers.las.filename='{clipped_laz}'",
        shell=True,
    )
    return clipped_laz




if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    WESM_BUCKET = "wesm"
    DATA_DIR = "data"
    CLIP_DIR = f"{DATA_DIR}/clips/{os.path.basename(IN_FILE).split('.')[0]}"
    BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}"  
    HEXBIN_DIR = f"{DATA_DIR}/hexbin/{STATE}/{WORKUNIT}"
    HEXBIN_DIR_TMP = f"{DATA_DIR}/hexbin/{STATE}/{WORKUNIT}/tmp"
    PIPELINE_CROP_PATH = 'process/pipeline-templates/buffer-clip-filter-template-crop-only.json'
    INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
    INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"

    for d in [DATA_DIR, BCM_DIR, HEXBIN_DIR, HEXBIN_DIR_TMP, CLIP_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()