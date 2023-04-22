import boto3
import geopandas as gp
import json
import subprocess as sub
import os
from shapely.geometry import Polygon
from pyproj import CRS
import sys

# python3 index/index-laz.py data/laz/tahoe-2018-10n

def main():
    s3 = get_creds()
    
    pages = get_pages(s3)

    df = []
    for page in pages:
        for obj in page['Contents']:
            file_prefix = obj['Key']
            if file_prefix.lower().endswith('.las') or file_prefix.lower().endswith('.laz'):
                
                laz_json = get_metadata(s3, file_prefix)                
                minx, miny, maxx, maxy, poly = bbox(laz_json)
                
                proj4 = laz_json['summary']['srs']['proj4']
                pointCount = laz_json['summary']['num_points']
                crs = f"epsg:{CRS.to_epsg(CRS.from_proj4(proj4))}"

                # Write to geoDataFrame
                print("Writing GeoDataFrame")
                df.append(
                    {
                        'bucket': DFBUCKET,
                        'prefix': file_prefix,
                        'workunit': WORKUNIT,
                        'crs': crs,
                        'minx': minx,
                        'maxx': maxx,
                        'miny': miny,
                        'maxy': maxy,
                        'proj4': proj4,
                        'point_count': pointCount,    
                        'native_poly': str(poly),   
                        'geometry': poly
                    }
                )            
                os.remove(file_prefix)
                
    gfd = gp.GeoDataFrame(df, crs=crs)
    gfd.to_crs(ALBERS_EPSG).to_file(f"{PREFIX_PATH}/{WORKUNIT}.gpkg", driver="GPKG")
    print(f"Uploading index gpkg: {PREFIX_PATH}/{WORKUNIT}.gpkg")
    s3.upload_file(f"{PREFIX_PATH}/{WORKUNIT}.gpkg", DFBUCKET, f"{INDEX_PATH}/laz/{WORKUNIT}.gpkg")
    
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

def get_pages(s3):
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=DFBUCKET, Prefix=PREFIX_PATH, ) # PaginationConfig={'MaxItems': 1}
    return pages

def get_metadata(s3, file_prefix):
    part_laz = s3.get_object(Bucket=DFBUCKET, Key=file_prefix, Range="bytes=0-10000")
    body = part_laz["Body"].read()
    with open(f"{file_prefix}", "wb") as f:
        f.write(body)
    
    # read laz metadata
    print("Read partial LAZ Metadata")
    pdalinfo = """
    pdal info --summary %s
    """ % (f"{file_prefix}")
    laz_meta = sub.check_output(pdalinfo, shell=True)
    laz_json = json.loads(laz_meta) 
    
    return laz_json
        
def bbox(laz_json):    
    minx = laz_json['summary']['bounds']['minx']
    miny = laz_json['summary']['bounds']['miny']
    maxx = laz_json['summary']['bounds']['maxx']
    maxy = laz_json['summary']['bounds']['maxy']
    
    poly = Polygon([[minx, miny],
                    [maxx, miny],
                    [maxx, maxy],
                    [minx, maxy],
                    [minx, miny]])
    
    return minx, miny, maxx, maxy, poly



if __name__ == "__main__":
    PREFIX_PATH = sys.argv[1]
    DFBUCKET = "synth-chm"
    WORKUNIT = PREFIX_PATH.split("/")[-1]
    ALBERS_EPSG = 3310
    INDEX_PATH = "index"

    os.makedirs(PREFIX_PATH, exist_ok=True)
    
    main()