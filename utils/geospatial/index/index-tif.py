import boto3
import geopandas as gp
import os
from shapely.geometry import Polygon
from pyproj import CRS
import sys
from osgeo import gdal
import rasterio as rio

# python3 src/geospatial/index/index-tif.py data/satellite/naip-3310

PREFIX_PATH = sys.argv[1]
DFBUCKET = "synth-chm"
WORKUNIT = PREFIX_PATH.split("/")[-1]
ALBERS_EPSG = 3310
index_path = "index"

os.makedirs(PREFIX_PATH, exist_ok=True)

# set AWS credentials
session = boto3.Session(profile_name='synth')
credentials = session.get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=DFBUCKET, Prefix=PREFIX_PATH, ) # PaginationConfig={'MaxItems': 1}

df = []
for page in pages:
    for obj in page['Contents']:
        file_prefix = obj['Key']
        if file_prefix.endswith('.tiff') or file_prefix.endswith('.tif'):
            with rio.Env(session):
                ds = rio.open(f"s3://{DFBUCKET}/{file_prefix}")
                crs = ds.crs
                bounds = ds.bounds
                minx = bounds[0]
                maxx = bounds[2]
                miny = bounds[1]
                maxy = bounds[3]
                proj4 = CRS.to_proj4(CRS.from_string(str(crs).split(":")[1]))
            
            print("Getting bounds")
            def bbox(minx, miny, maxx, maxy):
                return Polygon([[minx, miny],
                                [maxx, miny],
                                [maxx, maxy],
                                [minx, maxy],
                                [minx, miny]])

            runBbox = bbox(minx, miny, maxx, maxy)
            
            # Reproject bbox to Albers for uniformity
                       

            # Write to geoDataFrame
            print("Writing GeoDataFrame")
            df.append(
                {
                    'bucket': DFBUCKET,
                    'prefix': file_prefix,
                    'workunit': WORKUNIT,
                    'crs': str(crs),
                    'minx': minx,
                    'maxx': maxx,
                    'miny': miny,
                    'maxy': maxy,
                    'proj4': proj4,
                    'point_count': "NULL",
                    'native_poly': str(runBbox),   
                    'geometry': runBbox
                }
            )
            
gfd = gp.GeoDataFrame(df, crs=str(crs).split(":")[1])
gfd.to_crs(ALBERS_EPSG).to_file(f"{PREFIX_PATH}/{WORKUNIT}.gpkg", driver="GPKG")
print(f"Uploading index gpkg: {PREFIX_PATH}/{WORKUNIT}.gpkg")
s3.upload_file(f"{PREFIX_PATH}/{WORKUNIT}.gpkg", DFBUCKET, f"{index_path}/satellite/{WORKUNIT}.gpkg")