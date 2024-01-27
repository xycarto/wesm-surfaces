import boto3
import os
import subprocess as sub
import json
from osgeo import gdal
import geopandas as gp
from globals import *

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

def get_grid_index(s3, grid_bucket, grid_index, surface_index):
    if not os.path.exists(surface_index):
        s3.download_file(grid_bucket, grid_index, surface_index, ExtraArgs={'RequestPayer':'requester'})

class get_pc_metadata:
    def __init__(self, pc):
        print("Getting Metadata...")
        pc_metadata = sub.check_output(
            f"pdal info --summary '{pc}'",
            shell=True,
        )
        
        pc_json = json.loads(pc_metadata)
        
        self.minx = pc_json['summary']['bounds']['minx']
        self.miny = pc_json['summary']['bounds']['miny']
        self.maxx = pc_json['summary']['bounds']['maxx']
        self.maxy = pc_json['summary']['bounds']['maxy']
        self.proj4 = pc_json['summary']['srs']['proj4']
        self.wkt = pc_json['summary']['srs']['wkt']
        self.bounds = f"'([{self.minx}, {self.maxx}],[{self.miny}, {self.maxy}])'"

        self.width = int(abs(abs(self.maxx) - abs(self.minx)) / RESOLUTION)
        self.height = int(abs(abs(self.maxy) - abs(self.miny)) / RESOLUTION)
        
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

def make_tin(pipeline, in_pc, wkt, out_tif, metadata):
    sub.call(
        f"pdal pipeline '{pipeline}' \
            --readers.las.filename='{in_pc}' \
            --readers.las.spatialreference='{wkt}' \
            --filters.faceraster.resolution='{RESOLUTION}' \
            --filters.faceraster.origin_x='{metadata.minx}' \
            --filters.faceraster.origin_y='{metadata.miny}' \
            --filters.faceraster.width='{metadata.width}' \
            --filters.faceraster.height='{metadata.height}' \
            --writers.raster.filename='{out_tif}'",
        shell=True,
    )

def build_vrt(vrt_dir, vrt):
    print("Making VRT...")
    tifs = [f"{vrt_dir}/{tif}" for tif in os.listdir(vrt_dir) if not os.path.isdir(tif) and tif.endswith('.tif')]
    gdal.BuildVRT(
        vrt,
        tifs,
        resolution='average'
    ) 

def gdal_clip(data_dir, basename, in_file, index, in_tif, out_tif):
    index_file = gp.read_file(index)
    index_row = index_file[index_file['file_name'] == os.path.basename(in_file)]    
    index_repro = index_file.to_crs(index_row.native_horiz_crs.values[0])
    index_repro_row = index_repro[index_repro['file_name'] == os.path.basename(in_file)]

    tmp_gpkg = f"{data_dir}/{basename}.gpkg"
    gp.GeoDataFrame(index_repro_row.geometry).to_file(tmp_gpkg, driver="GPKG")  

    gdal.Warp(
        out_tif,
        in_tif,
        cutlineDSName = tmp_gpkg,
        cropToCutline = True,
        callback=gdal.TermProgress_nocb
    )

    return tmp_gpkg, out_tif