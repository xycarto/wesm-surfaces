import os
import subprocess
import geopandas as gp
from shapely.geometry import Polygon
import pandas as pd
import sys
import boto3
import numpy as np
from osgeo import gdal
import shutil

# python3 gridding/grid-clip-laz.py tahoe-2018-10n grid/412322

def main():    
    s3 = get_creds()

    print("Downloading Grid and Index...")
    grid, index_file = get_index(s3, GRID_PATH, INDEX_PATH) 
      
    print("Reading Grid and Index...")  
    gp_grid = gp.read_file(grid)
    gp_index = gp.read_file(index_file).to_crs(3310)
    
    cell = gp_grid[gp_grid['s3_prefix'] == GRID_CELL]    
    
    selection = get_intersect(cell, gp_index)
    
    print("Downloading Files...")
    cell_dir = f"{GRID_PATH}/{cell.grid_num.values[0]}"
    os.makedirs(cell_dir, exist_ok=True)
    select_array = [download_files(s3, dl) for indi, dl in selection.iterrows()]
    
    minx = cell['xmin']
    miny = cell['ymin']
    maxx = cell['xmax']
    maxy = cell['ymax']

    print("Building VRT...")
    print(select_array)
    # vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic')
    gdal.BuildVRT(
        f"{cell_dir}/{str(cell.grid_num.values[0])}.vrt", 
        select_array
    )
        
    print("Clipping VRT...")
    grid_chm = f"{cell_dir}/chm_{str(cell.grid_num.values[0])}.tif"
    gdal.Translate(
        grid_chm,
        f"{cell_dir}/{str(cell.grid_num.values[0])}.vrt",
        projWin=[minx, maxy, maxx, miny],
        outputBounds=[minx, maxy, maxx, miny]
    )

    print(f"Uploading {grid_chm}...")
    s3.upload_file(grid_chm, DFBUCKET, grid_chm)

    # # shutil.rmtree(cell_dir)
    
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

def get_index(s3, GRID_PATH, INDEX_PATH):
    # Load Grid
    grid = f"{GRID_PATH}/{WORKUNIT}_grid.gpkg"
    if not os.path.exists(grid):
        s3.download_file(DFBUCKET, grid, grid, ExtraArgs={'RequestPayer':'requester'})
        
    # Load Index
    index_file = f"{INDEX_PATH}/{WORKUNIT}.gpkg"
    if not os.path.exists(index_file):
        s3.download_file(DFBUCKET, index_file, index_file, ExtraArgs={'RequestPayer':'requester'})
        
    return grid, index_file

def get_intersect(cell, gp_index):
    cell_geom = cell.geometry.values[0]
    mask = gp_index.intersects(cell_geom)
    selection = gp_index.loc[mask]
    
    return selection

def download_files(s3, dl):
    chm_file = f"{CHM_PATH}/{os.path.basename(dl.prefix).split('.')[0]}.tif"
    print("Downloading Intersect Files...")
    if not os.path.exists(chm_file):
        s3.download_file(DFBUCKET, chm_file, chm_file, ExtraArgs={'RequestPayer':'requester'})
        
    return chm_file

if __name__ == "__main__":
    WORKUNIT = sys.argv[1]
    GRID_CELL = sys.argv[2]
    DFBUCKET = "synth-chm"
    CHM_PATH = f"data/chm/{WORKUNIT}"
    GRID_PATH = "grid"
    INDEX_PATH = "index/laz"
    LIST_PATH = "lists"

    os.makedirs(GRID_PATH, exist_ok=True)
    os.makedirs(INDEX_PATH, exist_ok=True)
    os.makedirs(CHM_PATH, exist_ok=True)
    
    main()