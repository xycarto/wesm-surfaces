import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gp
import subprocess as sub
from shapely.geometry import Polygon
import pandas as pd
import sys
import boto3
import numpy as np
from osgeo import gdal
import shutil
from multiprocessing import Pool

# python3 gridding/grid-clip-naip.py data/satellite/naip-3310


def main(NAIP_PATH, WORKUNIT, DFBUCKET, GRID_PATH, INDEX_PATH):
    
    print("Setting Creds...")
    s3 = get_creds()
    
    print("Downloading Grid and Index...")
    grid, index_file = get_index(s3, GRID_PATH, INDEX_PATH) 
       
    print("Intersecting Grid and Index...")
    grid_select, gp_index = get_intersect(grid, index_file)    

    print("Looping Grid Cells...")
    with Pool(8) as pool:
        items = [(grid_cell, gp_index, GRID_PATH, NAIP_PATH, DFBUCKET) for index, grid_cell in grid_select.iterrows()]
        pool.starmap(process, items)  
        
        
def process(grid_cell, gp_index, GRID_PATH, NAIP_PATH, DFBUCKET):
    
    s3_tmp = get_creds()
    
    print("Intersecting...")
    selection = cell_intersection(grid_cell, gp_index)        
    
    cell_dir = f"{GRID_PATH}/{grid_cell.grid_num}"        
    os.makedirs(cell_dir, exist_ok=True)
    
    print("Building Array for VRT...")
    select_array = [
        build_vrt_array(dl, NAIP_PATH, s3_tmp, DFBUCKET, grid_cell) for indi, dl in selection.iterrows()
        ]
        
    print("Building VRT...")         
    build_vrt(select_array, NAIP_PATH, grid_cell)
    
    print("Clipping VRT...")
    grid_naip = clip_vrt(cell_dir, grid_cell, NAIP_PATH)
    
    print(f"Uploading {grid_naip}...")
    s3_tmp.upload_file(grid_naip, DFBUCKET, grid_naip)
    
    tmp_dir = f"{NAIP_PATH}/{grid_cell.grid_num}"
    shutil.rmtree(tmp_dir)
    shutil.rmtree(cell_dir)


def get_creds():

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

def get_index(s3, GRID_PATH, INDEX_PATH):
    # Load Grid
    grid = f"{GRID_PATH}/grid_index.gpkg"
    if not os.path.exists(grid):
        s3.download_file(DFBUCKET, grid, grid, ExtraArgs={'RequestPayer':'requester'})
        
    # Load Index
    index_file = f"{INDEX_PATH}/{WORKUNIT}.gpkg"
    if not os.path.exists(index_file):
        s3.download_file(DFBUCKET, index_file, index_file, ExtraArgs={'RequestPayer':'requester'})
        
    return grid, index_file

def get_intersect(grid, index_file):
    gp_index = gp.read_file(index_file)
    gp_index['diss'] = 1
    intersect_diss = gp_index.dissolve(by='diss')
    gp_grid = gp.read_file(grid)
    select = intersect_diss.geometry[1]
    grid_mask = gp_grid.intersects(select)
    grid_select = gp_grid.loc[grid_mask]
    
    return grid_select, gp_index

def cell_intersection(grid_cell, gp_index):
    cell_geom = grid_cell.geometry
    mask = gp_index.intersects(cell_geom)
    selection = gp_index.loc[mask]
    
    return selection

def build_vrt_array(dl, NAIP_PATH, s3_tmp, DFBUCKET, grid_cell):
    
    tmp_hold = f"{NAIP_PATH}/{grid_cell.grid_num}"
    os.makedirs(tmp_hold, exist_ok=True)
    
    prefix = dl.prefix
    naip_file = f"{NAIP_PATH}/{os.path.basename(prefix).split('.')[0]}.tif"
    naip_file_local = f"{tmp_hold}/{os.path.basename(prefix).split('.')[0]}.tif"
    if not os.path.exists(naip_file):
        s3_tmp.download_file(DFBUCKET, naip_file, naip_file_local, ExtraArgs={'RequestPayer':'requester'})
    edit_cmd = """
        gdal_edit.py -a_nodata 0 %s
    """ % (naip_file_local)
    sub.call(edit_cmd, shell=True)
        
    return naip_file_local

def build_vrt(select_array, NAIP_PATH, grid_cell):
    vrt_options = gdal.BuildVRTOptions(resampleAlg='bilinear')
    gdal.BuildVRT(
        f"{NAIP_PATH}/{str(grid_cell.grid_num)}.vrt", 
        select_array, 
        options=vrt_options
    )
    
def clip_vrt(cell_dir, grid_cell, NAIP_PATH):   
    minx = grid_cell['xmin']
    miny = grid_cell['ymin']
    maxx = grid_cell['xmax']
    maxy = grid_cell['ymax']
    grid_naip = f"{cell_dir}/naip_{str(grid_cell.grid_num)}.tif"
    gdal.Translate(
        grid_naip,
        f"{NAIP_PATH}/{str(grid_cell.grid_num)}.vrt",
        projWin=[minx, maxy, maxx, miny],
        outputBounds=[minx, maxy, maxx, miny]
    ) 
    
    return grid_naip

   
if __name__ == "__main__":
    
    NAIP_PATH = sys.argv[1]
    WORKUNIT = NAIP_PATH.split("/")[-1]
    DFBUCKET = os.environ.get("AWS_BUCKET")
    GRID_PATH = "grid"
    INDEX_PATH = "index/satellite"

    os.makedirs(GRID_PATH, exist_ok=True)
    os.makedirs(INDEX_PATH, exist_ok=True)
    os.makedirs(NAIP_PATH, exist_ok=True)
    
    main(NAIP_PATH, WORKUNIT, DFBUCKET, GRID_PATH, INDEX_PATH)
