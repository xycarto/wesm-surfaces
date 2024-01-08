import boto3
import os
import subprocess as sub
import json
from osgeo import gdal

def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name = 'us-west-2',
    )

    return s3

def get_s3_file(s3, file, bucket):
    if not os.path.exists(file):
        s3.download_file(bucket, file, file, ExtraArgs={'RequestPayer':'requester'})

class get_pc_metadata:
    def __init__(self, pc):
        print("Getting Metadata...")
        pc_metadata = sub.check_output(
            f"pdal info --summary '{pc}'",
            shell=True,
        )
        
        pc_json = json.loads(pc_metadata)
        
        minx = pc_json['summary']['bounds']['minx']
        miny = pc_json['summary']['bounds']['miny']
        maxx = pc_json['summary']['bounds']['maxx']
        maxy = pc_json['summary']['bounds']['maxy']
        self.proj4 = pc_json['summary']['srs']['proj4']
        self.wkt = pc_json['summary']['srs']['wkt']
        self.bounds = f"'([{minx}, {maxx}],[{miny}, {maxy}])'"
        
def get_bound_info(pc):
    pc_metadata = sub.check_output(
        f"pdal info --summary '{pc}'",
        shell=True,
    )
    
    pc_json = json.loads(pc_metadata)
    
    minx = pc_json['summary']['bounds']['minx']
    miny = pc_json['summary']['bounds']['miny']
    maxx = pc_json['summary']['bounds']['maxx']
    maxy = pc_json['summary']['bounds']['maxy']
    
    return minx, miny, maxx, maxy

def make_surface(pipeline, in_pc, wkt, out_tif, bounds):
    sub.call(
        f"pdal pipeline '{pipeline}' \
            --readers.las.filename='{in_pc}' \
            --readers.las.spatialreference='{wkt}' \
            --writers.gdal.filename='{out_tif}' \
            --writers.gdal.bounds={bounds}",
        shell=True,
    )

def build_vrt(vrt_dir, vrt):
    print("Making VRT...")
    tifs = [f"{os.path.join(vrt_dir, tif)}" for tif in os.listdir(vrt_dir) if not os.path.isdir(tif) and tif.endswith('.tif')]

    gdal.BuildVRT(
        vrt,
        tifs,
        resolution='average'
    ) 