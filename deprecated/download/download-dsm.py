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
        local_file = f"{DSM_DIR}/{os.path.basename(row.file_name).split('.')[0]}.tif"
        print(f"Downloading {local_file}")
        try: 
            if not os.path.exists(local_file):
                s3.download_file(WESM_SURFACE_BUCKET, local_file, local_file, ExtraArgs={'RequestPayer':'requester'})
        except:
            print("File Not Found")
        # if i >= 100:
        #     exit()
    
if __name__ == "__main__":

    USGS_BUCKET="usgs-lidar"
    WESM_SURFACE_BUCKET="xyc-wesm-surfaces"
    WESM_GRID_BUCKET="xyc-wesm-grids"
    CRS = "4269"
    WORKUNIT = sys.argv[1]
    STATE = sys.argv[2]
    TYPE = sys.argv[3]
    DATA_DIR = "data"
    DSM_DIR = f"{DATA_DIR}/dsm/{STATE}/{WORKUNIT}"
    INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
    INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_{CRS}.gpkg"

    for d in [DATA_DIR, DSM_DIR, INDEX_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()