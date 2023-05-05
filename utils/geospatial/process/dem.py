#!/usr/bin/env python
import os
import boto3
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import json

# python3 process/dem.py path/to/laz.laz


def main():
    s3 = get_creds()    
    bcm_laz = download_file(s3)
        
    proj4, bounds = get_metadata(bcm_laz)

    print("Creating DEM...")
    dem_file = f"{DEM_PATH}/{os.path.basename(IN_FILE).split('.')[0]}.tif"
    sub.call(
        f"pdal pipeline '{PIPELINE_PATH}' \
            --readers.las.filename='{bcm_laz}' \
            --readers.las.spatialreference='{proj4}' \
            --writers.gdal.filename='{dem_file}' \
            --writers.gdal.bounds={bounds}",
        shell=True,
    )

    print(f"Uploading {dem_file}...")
    s3.upload_file(dem_file, BUCKET, dem_file)

   
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

def download_file(s3):
    bcm_laz = f"{BCM_PATH}/{os.path.basename(IN_FILE)}"
    if not os.path.exists(f'{bcm_laz}'):
        print("Downloading BCM...")
        s3.download_file(BUCKET, bcm_laz, bcm_laz, ExtraArgs={'RequestPayer':'requester'})
        
    return bcm_laz

def get_metadata(bcm_laz):
    print("Getting Metadata...")
    laz_metadata = sub.check_output(
        f"pdal info --summary '{bcm_laz}'",
        shell=True,
    )
    
    laz_json = json.loads(laz_metadata)
    
    minx = laz_json['summary']['bounds']['minx']
    miny = laz_json['summary']['bounds']['miny']
    maxx = laz_json['summary']['bounds']['maxx']
    maxy = laz_json['summary']['bounds']['maxy']
    proj4 = laz_json['summary']['srs']['proj4']
    bounds = f"'([{minx}, {maxx}],[{miny}, {maxy}])'"
    
    return proj4, bounds

if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    WORKUNIT =IN_FILE.split('/')[-2]
    BUCKET = os.environ.get("AWS_BUCKET")
    LAZ_PATH = f"data/laz/{WORKUNIT}"
    DEM_PATH = f"data/dem/{WORKUNIT}"
    BCM_PATH = f"data/bcm/{WORKUNIT}"
    PIPELINE_PATH = 'process/pipeline-templates/dem_template.json'

    os.makedirs(LAZ_PATH, exist_ok=True)
    os.makedirs(DEM_PATH, exist_ok=True)
    os.makedirs(BCM_PATH, exist_ok=True)
    
    main()