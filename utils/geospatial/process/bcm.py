#!/usr/bin/env python
import os
import boto3
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import shutil

# python3 process/bcm.py data/laz/tahoe-2018-10n/laz_tahoe_tile_-6000_135000_denoised_ground_norm_classify_seamless.laz
# python3 process/bcm.py data/laz/tahoe-2018-10n/laz_tahoe_tile_-6000_136000_denoised_ground_norm_classify_seamless.laz
# python3 process/bcm.py data/laz/tahoe-2018-10n/laz_tahoe_tile_-7000_136000_denoised_ground_norm_classify_seamless.laz
# python3 process/bcm.py data/laz/tahoe-2018-10n/laz_tahoe_tile_-7000_135000_denoised_ground_norm_classify_seamless.laz

def main():
    s3 = get_creds()
    gp_index = get_index(s3)    

    # Buffer Index
    row = gp_index[gp_index['prefix'] == IN_FILE]    
    row_buff = row.geometry.buffer(BUFFER, join_style=2)

    tiles_select = gp_index.loc[gp_index.intersects(row_buff.geometry.values[0])]
    
    clipped_array = [clip_files(row, row_buff, s3, laz) for i, laz in tiles_select.iterrows()]
     
    # Merge point clouds
    bcm_laz = merge_pc(clipped_array)

    # filter LAZ
    filtered_laz = filter_laz(bcm_laz, row)
        
    print(f"Uploading... {filtered_laz}")   
    s3.upload_file(filtered_laz, DFBUCKET, filtered_laz)

    # shutil.rmtree(CLIP_PATH)
    # shutil.rmtree(BCM_PATH)    

    # os.makedirs(LAZ_PATH, exist_ok=True)
    # os.makedirs(BCM_PATH, exist_ok=True)
    
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

def get_index(s3):
    # Get Index file and load as Geopandas
    INDEX_PREFIX = f"index/laz/{WORKUNIT}.gpkg"
    INDEX_LOCAL = f'{LAZ_PATH}/{WORKUNIT}.gpkg'
    if not os.path.exists(f'{LAZ_PATH}/{WORKUNIT}.gpkg'):
        s3.download_file(DFBUCKET, INDEX_PREFIX, INDEX_LOCAL, ExtraArgs={'RequestPayer':'requester'})
    gp_index = gp.read_file(INDEX_LOCAL)
    
    return gp_index

def download_laz(s3, laz, in_laz):
    if not os.path.exists(in_laz):
        print(f"Downloading: {laz.prefix}...")
        s3.download_file(DFBUCKET, laz.prefix, in_laz, ExtraArgs={'RequestPayer':'requester'})
        
def clip_files(row, row_buff, s3, laz):
    # Clip Merged File
    print(f"Clipping Input Point Cloud...")
    os.makedirs(CLIP_PATH, exist_ok=True)
    in_laz = f"{CLIP_PATH}/{os.path.basename(laz.prefix)}"
    download_laz(s3, laz, in_laz)
    clipped_laz = f"{CLIP_PATH}/{os.path.basename(laz.prefix).split('.')[0]}_tmp_crop.laz"
    if laz.prefix != IN_FILE:
        sub.call(
            f"pdal pipeline '{PIPELINE_CROP}' \
                --readers.las.filename='{in_laz}' \
                --filters.crop.polygon='{row_buff.geometry.values[0]}' \
                --writers.las.filename='{clipped_laz}'",
            shell=True,
        )
        return clipped_laz
    else:    
        return in_laz

def merge_pc(clipped_array):       
    print("Merging...")
    bcm_laz = f"{BCM_PATH}/{os.path.basename(IN_FILE).split('.')[0]}_merged.laz"
    sub.call(
        f"""pdal merge {" ".join(clipped_array)} {bcm_laz}""",
        shell=True,
    )
    return bcm_laz

def filter_laz(bcm_laz, row):
    print("Filtering...")   
    filtered_laz =  f"{BCM_PATH}/{os.path.basename(IN_FILE)}"
    sub.call(
        f"pdal pipeline '{PIPELINE_FILTER}' \
            --readers.las.filename='{bcm_laz}' \
            --writers.las.filename='{filtered_laz}' \
            --writers.las.a_srs='{row.proj4.values[0]}'",
        shell=True,
    )
    
    # os.remove(bcm_laz)
    return filtered_laz
   
if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT =IN_FILE.split('/')[-2]
    DFBUCKET = "synth-chm"
    LAZ_PATH = f"data/laz/{WORKUNIT}"
    BCM_PATH = f"data/bcm/{WORKUNIT}"        
    CLIP_PATH = f"{LAZ_PATH}/{os.path.basename(IN_FILE).split('.')[0]}"
    BUFFER = 50
    PIPELINE_CROP = 'process/pipeline-templates/buffer-clip-filter-template-crop-only.json'
    PIPELINE_FILTER = 'process/pipeline-templates/buffer-clip-filter-template-filter-only.json'

    os.makedirs(LAZ_PATH, exist_ok=True)
    os.makedirs(BCM_PATH, exist_ok=True)
    
    main()