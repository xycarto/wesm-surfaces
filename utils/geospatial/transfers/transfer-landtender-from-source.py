import boto3
import os
import geopandas as gp
import sys
from osgeo import gdal

# python3 src/geospatial/transfers/transfer-landtender-from-source.py data/merged-naip-tahoe-select.gpkg

VPBUCKET = 'vibrant-dragon'
DFBUCKET = "synth-chm"

ltBUCKET = "naip-analytic"

index_file = sys.argv[1]
base_path = 'data/naip-temp'
# index_name = os.path.basename(index_file).split(".")[0]
# base_path_ca = f"ca/60cm/rgbir_cog"
os.makedirs(base_path, exist_ok=True)

print("Setting credentials")
# set AWS credentials for VP
sess_vp = boto3.Session(profile_name='vpTemp')
creds_vp = sess_vp.get_credentials()
access_key_vp = creds_vp.access_key
secret_key_vp = creds_vp.secret_key

s3_vp = boto3.client(
    's3',
    aws_access_key_id=access_key_vp,
    aws_secret_access_key=secret_key_vp,
)

# set AWS credentials for DF
sess_df = boto3.Session(profile_name='synth')
creds_df = sess_df.get_credentials()
access_key_df = creds_df.access_key
secret_key_df = creds_df.secret_key

s3_df = boto3.client(
    's3',
    aws_access_key_id=access_key_df,
    aws_secret_access_key=secret_key_df,
)

gp_index = gp.read_file(index_file)
for index, row in gp_index.iterrows():
    file_name = f"m_{row.USGSID}_{row.QUAD.lower()}_{row.ZONE}_0{row.RES}_{row.SrcImgDate}.tif"
    state = row.ST.lower()
    year = str(row.SrcImgDate)[:4]
    prefix = f"{state}/{year}/60cm/rgbir_cog/{str(row.USGSID)[:5]}/{file_name}"  
    print(prefix)
    try:
        if not os.path.exists(f'{base_path}/{file_name}'):
            s3_vp.download_file(ltBUCKET, prefix, f'{base_path}/{file_name}', ExtraArgs={'RequestPayer':'requester'})
        
        print("Reprojecting to Albers")    
        gdal.Warp(
            f"{base_path}/m_{row.USGSID}_{row.QUAD.lower()}_{row.ZONE}_0{row.RES}_{row.SrcImgDate}-3310.tif",
            f'{base_path}/{file_name}',
            xRes = 0.5,
            yRes = 0.5,
            dstSRS = "EPSG:3310",
            resampleAlg = 'cubic'
        )
        
        print("Uploading to DF S3")
        s3_df.upload_file(f"{base_path}/m_{row.USGSID}_{row.QUAD.lower()}_{row.ZONE}_0{row.RES}_{row.SrcImgDate}-3310.tif", DFBUCKET, f"data/satellite/naip-3310/m_{row.USGSID}_{row.QUAD.lower()}_{str(row.ZONE)}_0{row.RES}_{row.SrcImgDate}-3310.tif")
        
        os.remove(f'{base_path}/{file_name}')
        os.remove(f"{base_path}/m_{row.USGSID}_{row.QUAD.lower()}_{row.ZONE}_0{row.RES}_{row.SrcImgDate}-3310.tif")
    except:
        print(f"Invalid. Skipping.... {prefix}")
        continue
    
    # if index <= 0:
    #     break
