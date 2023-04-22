import boto3
import os

# python3 src/geospatial/transfer-landtender.py

VPBUCKET = 'vibrant-dragon'
DFBUCKET = "synth-chm"

lt_vp = "naip20_tahoe_landtender/cubic_50cm/nv19_and_ca20/"

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

# List VP S3
paginator = s3_vp.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=VPBUCKET, Prefix=lt_vp, ) # PaginationConfig={'MaxItems': 1}

for page in pages:
    for obj in page['Contents']:
        filePREFIX = obj['Key']
        print(f'Transferring: {filePREFIX}')
        dir_path = os.path.dirname(filePREFIX)
        os.makedirs(f'tmp/{dir_path}', exist_ok=True)
        base_name = os.path.basename(filePREFIX)
        s3_vp.download_file(VPBUCKET, filePREFIX, f'tmp/{filePREFIX}')
        s3_df.upload_file(f'tmp/{filePREFIX}', DFBUCKET, filePREFIX)
        os.remove(f'tmp/{filePREFIX}')