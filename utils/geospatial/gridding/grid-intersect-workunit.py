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

# python3 gridding/grid-intersect-workunit.py tahoe-2018-10n


def main():
    s3 = get_creds()

    # Load Grid
    grid = f"{GRID_PATH}/grid_index.gpkg"
    if not os.path.exists(grid):
        s3.download_file(DFBUCKET, grid, grid, ExtraArgs={'RequestPayer':'requester'})
        
    # Load Index
    index_file = f"{INDEX_PATH}/{WORKUNIT}.gpkg"
    if not os.path.exists(index_file):
        s3.download_file(DFBUCKET, index_file, index_file, ExtraArgs={'RequestPayer':'requester'})
        
    # Find Available Files in Index, Create GPKG
    wu_list = open(f"{LIST_PATH}/{WORKUNIT}.txt",'r')
    gp_index = gp.read_file(index_file)
    alber_index = gp_index.to_crs(3310)
    found = []
    for i in wu_list:
        row = alber_index[alber_index['prefix'] == f"{i.strip().replace('bcm','laz')}"]
        found.append(row.iloc[0])
    
    #  Intersect index area with grid    
    intersect_rows = gp.GeoDataFrame(found, crs='epsg:3310')
    intersect_rows['diss'] = 1
    intersect_diss = intersect_rows.dissolve(by='diss')
    gp_grid = gp.read_file(grid)
    select = intersect_diss.geometry[1]
    grid_mask = gp_grid.intersects(select)
    grid_select = gp_grid.loc[grid_mask]

    grid_select.to_file(f"{GRID_PATH}/{WORKUNIT}_grid.gpkg", driver="GPKG")

    # print(f"Uploading {grid_chm}...")
    s3.upload_file(f"{GRID_PATH}/{WORKUNIT}_grid.gpkg", DFBUCKET, f"{GRID_PATH}/{WORKUNIT}_grid.gpkg")

    with open(f"{LIST_PATH}/{WORKUNIT}_grid.txt",'w') as grid_list:
        for index, row in grid_select.iterrows():
            grid_list.write(row.s3_prefix)
            grid_list.write('\n')
            
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

if __name__ == "__main__":
    WORKUNIT = sys.argv[1]
    DFBUCKET = "synth-chm"
    GRID_PATH = "grid"
    INDEX_PATH = "index/laz"
    LIST_PATH = "lists"

    os.makedirs(GRID_PATH, exist_ok=True)
    os.makedirs(INDEX_PATH, exist_ok=True)
    
    main()