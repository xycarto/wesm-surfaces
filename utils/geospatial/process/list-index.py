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

# python3 process/list-index.py tahoe-2018-10n

# set AWS credentials

def main():    
    # get creds
    s3 = get_creds()
    
    # Get Index file and load as Geopandas
    s3.download_file(BUCKET, INDEX_PREFIX, INDEX_PREFIX, ExtraArgs={'RequestPayer':'requester'})
    gp_index = gp.read_file(INDEX_PREFIX)

    with open(f"{LIST_PATH}/{WORKUNIT}.txt",'w') as grid_list:
        for index, row in gp_index.iterrows():
            grid_list.write(row.prefix)
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
    BUCKET = "xycarto"
    LAZ_PATH = f"data/laz/{WORKUNIT}"
    INDEX_PATH = "index/laz"
    INDEX_PREFIX = f"{INDEX_PATH}/{WORKUNIT}.gpkg"
    LIST_PATH = "lists"

    for dr in (LAZ_PATH, LIST_PATH, INDEX_PATH):
        os.makedirs(dr, exist_ok=True)
        
    main()
