import boto3
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gp
import sys
sys.path.append('pyutils')
from general import *


def main():    
    s3 = get_creds()
    get_s3_file(s3, INDEX_FILE, WESM_GRID_BUCKET)

    # list available rows
    index_file = gp.read_file(INDEX_FILE)
    for i, row in index_file.iterrows():
        local_file = f"{BCM_DIR}/{row.file_name}"
        print(f"Downloading {local_file}")
        if not os.path.exists(local_file):
            s3.download_file(WESM_SURFACE_BUCKET, local_file, local_file, ExtraArgs={'RequestPayer':'requester'})
        if i >= 12:
            exit()
    
if __name__ == "__main__":

    USGS_BUCKET="usgs-lidar"
    WESM_SURFACE_BUCKET="xyc-wesm-surfaces"
    WESM_GRID_BUCKET="xyc-wesm-grids"
    CRS = "4269"
    WORKUNIT = sys.argv[1]
    STATE = sys.argv[2]
    DATA_DIR = "data"
    BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}"
    TIN_DIR = f"{DATA_DIR}/tin/{STATE}/{WORKUNIT}"
    DSM_DIR = f"{DATA_DIR}/dsm/{STATE}/{WORKUNIT}"
    INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
    INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_{CRS}.gpkg"

    for d in [DATA_DIR, BCM_DIR, TIN_DIR, DSM_DIR, INDEX_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()