#!/usr/bin/env python
import os
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import shutil
from py_utils import *
from globals import *

# Example Single file: make bcm pc=Projects/CA_NoCAL_3DEP_Supp_Funding_2018_D18/CA_NoCAL_Wildfires_B1_2018/LAZ/USGS_LPC_CA_NoCAL_3DEP_Supp_Funding_2018_D18_w2021n2061.laz workunit=CA_NoCAL_Wildfires_B1_2018 state=California

# Example Multi File: time make test-local workunit=CA_NoCAL_Wildfires_B1_2018 state=California process=bcm ec2=t2.large volume_size=20 type=test 

def main():
    s3 = get_creds()
    get_grid_index(s3, WESM_GRID_BUCKET, GRID_INDEX_FILE, INDEX_FILE)

    # Buffer Index
    index_file = gp.read_file(INDEX_FILE)
    index_row = index_file[index_file['file_name'] == os.path.basename(IN_FILE)]    
    index_repro = index_file.to_crs(index_row.native_horiz_crs.values[0])
    index_repro_row = index_repro[index_repro['file_name'] == os.path.basename(IN_FILE)]
    row_buff = index_repro_row.geometry.buffer(BCM_BUFFER, join_style=2)

    # Select adjacent tiles, clip, and make array
    tiles_select = index_repro.loc[index_repro.intersects(row_buff.geometry.values[0])]
    clipped_array = [clip_files(row_buff, s3, pc) for i, pc in tiles_select.iterrows()]
    
    # Merge point clouds
    merged_pc = merge_pc(clipped_array)

    print(f"Uploading... {merged_pc}")   
    s3.upload_file(merged_pc, WESM_SURFACE_BUCKET, merged_pc)

    shutil.rmtree(CLIP_DIR)

    # os.remove(merged_pc)

def clip_files(row_buff, s3, pc):
    print(f"Clipping Input Point Cloud...")
    clip_in_file = os.path.join(PC_DIR, pc.file_name)
    clipped_laz = f"{CLIP_DIR}/{os.path.basename(clip_in_file).split('.')[0]}_tmp_crop.laz"
    if os.path.exists(clip_in_file) and clip_in_file != IN_FILE:
        sub.call(
            f"pdal -v 0 pipeline '{PIPELINE_CROP_FILTER}' \
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
    merged_pc = f"{BCM_DIR}/{os.path.basename(IN_FILE).split('.')[0]}.laz"
    sub.call(
        f"""pdal -v 0 merge {" ".join(clipped_array)} {merged_pc}""",
        shell=True,
    )
    return merged_pc

       
if __name__ == "__main__":

    IN_FILE = sys.argv[1]
    CLIP_DIR = f"{DATA_DIR}/clips/{os.path.basename(IN_FILE).split('.')[0]}"
        
    for d in [DATA_DIR, PC_DIR, BCM_DIR, CLIP_DIR, INDEX_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()