#!/usr/bin/env python
import os
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import shutil
sys.path.append('pyutils')
from general import *

def main():
    s3 = get_creds()
    get_s3_file(s3, INDEX_FILE, WESM_BUCKET)
    

    bcm = os.path.join(BCM_DIR, os.path.basename(IN_FILE))
    print(bcm)
    # if not os.path.exists(bcm):
    #     # Buffer Index
    #     index_file = gp.read_file(INDEX_FILE)
    #     index_row = index_file[index_file['file_name'] == os.path.basename(IN_FILE)]    
    #     index_repro = index_file.to_crs(index_row.native_horiz_crs.values[0])
    #     index_repro_row = index_repro[index_repro['file_name'] == os.path.basename(IN_FILE)]
    #     row_buff = index_repro_row.geometry.buffer(BUFFER, join_style=2)

    #     # Select adjacent tiles, clip, and make array
    #     tiles_select = index_repro.loc[index_repro.intersects(row_buff.geometry.values[0])]
    #     clipped_array = [clip_files(row_buff, s3, pc) for i, pc in tiles_select.iterrows()]
        
    #     # Merge point clouds
    #     merged_pc = merge_pc(clipped_array)

    #     # Filter LAZ
    #     bcm_file = filter_laz(merged_pc, index_row)

    #     shutil.rmtree(CLIP_DIR)
    #     os.remove(merged_pc)
            
    #     # print(f"Uploading... {filtered_laz}")   
    #     # s3.upload_file(filtered_laz, BUCKET, filtered_laz)


def clip_files(row_buff, s3, pc):
    print(f"Clipping Input Point Cloud...")
    clip_in_file = os.path.join(PC_DIR, pc.file_name)
    clipped_laz = f"{CLIP_DIR}/{os.path.basename(clip_in_file).split('.')[0]}_tmp_crop.laz"
    if clip_in_file != IN_FILE:
        print(clip_in_file)
        sub.call(
            f"pdal pipeline '{PIPELINE_CROP}' \
                --readers.las.filename='{clip_in_file}' \
                --filters.crop.polygon='{row_buff.geometry.values[0]}' \
                --writers.las.filename='{clipped_laz}'",
            shell=True,
        )
        return clipped_laz
    else:    
        return IN_FILE

def merge_pc(clipped_array):       
    print("Merging...")
    merged_pc = f"{CLIP_DIR}/{os.path.basename(IN_FILE).split('.')[0]}_merged.laz"
    sub.call(
        f"""pdal merge {" ".join(clipped_array)} {merged_pc}""",
        shell=True,
    )
    return merged_pc

def filter_laz(merged_pc, index_row):
    print("Filtering...")   
    bcm_file =  f"{BCM_DIR}/{os.path.basename(IN_FILE)}"
    crs = f"EPSG:{index_row.native_horiz_crs.values[0]}"
    sub.call(
        f"pdal pipeline '{PIPELINE_FILTER}' \
            --readers.las.filename='{merged_pc}' \
            --writers.las.filename='{bcm_file}' \
            --writers.las.a_srs='{crs}'",
        shell=True,
    )
    
    # os.remove(bcm_laz)
    return bcm_file
   
if __name__ == "__main__":

    IN_FILE = sys.argv[1]
    WORKUNIT = sys.argv[2]
    STATE = sys.argv[3]
    WESM_BUCKET = "wesm"
    DATA_DIR = "data"
    PC_DIR = os.path.join(DATA_DIR, "point-clouds", STATE, WORKUNIT)
    BCM_DIR = os.path.join(DATA_DIR, "bcm", STATE, WORKUNIT)        
    CLIP_DIR = os.path.join(DATA_DIR, "clips", f"{os.path.basename(IN_FILE).split('.')[0]}")
    INDEX_DIR = os.path.join(DATA_DIR, "index-indv", STATE)
    INDEX_FILE = os.path.join(INDEX_DIR, f"{WORKUNIT}_index_4269.gpkg")
    BUFFER = 50
    PIPELINE_CROP = 'process/pipeline-templates/buffer-clip-filter-template-crop-only.json'
    PIPELINE_FILTER = 'process/pipeline-templates/buffer-clip-filter-template-filter-only.json'

    
    for d in [DATA_DIR, PC_DIR, BCM_DIR, CLIP_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()