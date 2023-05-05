#!/usr/bin/env python
import os
import boto3
import geopandas as gp
import subprocess as sub
from pyproj import CRS
import sys
import json

# python3 process/dsm.py data/laz/tahoe-2018-10n/laz_tahoe_tile_-6000_135000_denoised_ground_norm_classify_seamless.laz
# python3 process/dsm.py data/laz/tahoe-2018-10n/laz_tahoe_tile_-6000_136000_denoised_ground_norm_classify_seamless.laz


def main():
    s3 = get_creds()    
    bcm_laz = download_file(s3)
        
    proj4, bounds = get_metadata(bcm_laz)
    
    print(proj4)
    print(bounds)

    print("Creating DSM...")
    dsm_file = f"{DSM_PATH}/{os.path.basename(IN_FILE).split('.')[0]}.tif"
    crs = f"epsg:{CRS.to_epsg(CRS.from_proj4(proj4))}"
    sub.call(
        f"pdal pipeline '{PIPELINE_PATH}' \
            --readers.las.filename='{bcm_laz}' \
            --readers.las.spatialreference='{proj4}' \
            --writers.gdal.filename='{dsm_file}' \
            --writers.gdal.bounds={bounds}",
        shell=True,
    )

    print(f"Uploading {dsm_file}...")
    s3.upload_file(dsm_file, DFBUCKET, dsm_file)

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
        s3.download_file(DFBUCKET, bcm_laz, bcm_laz, ExtraArgs={'RequestPayer':'requester'})
        
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
    DFBUCKET = "synth-chm"
    LAZ_PATH = f"data/laz/{WORKUNIT}"
    DSM_PATH = f"data/dsm/{WORKUNIT}"
    BCM_PATH = f"data/bcm/{WORKUNIT}"
    PIPELINE_PATH = 'process/pipeline-templates/dsm_template.json'

    os.makedirs(LAZ_PATH, exist_ok=True)
    os.makedirs(DSM_PATH, exist_ok=True)
    os.makedirs(BCM_PATH, exist_ok=True)
    
    main()