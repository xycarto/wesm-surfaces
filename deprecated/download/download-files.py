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
        bucket, in_file, local_file = set_paths(row)
        print(f"Downloading {local_file}")
        try: 
            if not os.path.exists(local_file):
                s3.download_file(bucket, in_file, local_file, ExtraArgs={'RequestPayer':'requester'})
        except:
            print("File Not Found")
        if TYPE == "test":
            if i >= 10:
                exit()
    
def set_paths(row):
    if PROCESS == "bcm":
        bucket = USGS_BUCKET
        in_file = row.usgs_loc
        local_file= os.path.join(PC_DIR, row.file_name)
    elif PROCESS == "surfaces":
        bucket = WESM_SURFACE_BUCKET
        in_file = f"{BCM_DIR}/{row.file_name}"
        local_file = in_file
    elif PROCESS == "solar":
        bucket = WESM_SURFACE_BUCKET
        in_file = f"{DSM_DIR}/{os.path.basename(row.file_name).split('.')[0]}.tif"
        local_file = in_file
    else:
        print("Unknown input...")
    
    return bucket, in_file, local_file

if __name__ == "__main__":

    USGS_BUCKET="usgs-lidar"
    WESM_SURFACE_BUCKET="xyc-wesm-surfaces"
    WESM_GRID_BUCKET="xyc-wesm-grids"
    CRS = "4269"
    WORKUNIT = sys.argv[1]
    STATE = sys.argv[2]
    PROCESS = sys.argv[3]
    TYPE = sys.argv[4]
    if TYPE == "test":
        DATA_DIR = "test-data"    
    else:
        DATA_DIR = "data"
    PC_DIR = f"{DATA_DIR}/point-clouds/{STATE}/{WORKUNIT}"
    BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}"
    TIN_DIR = f"{DATA_DIR}/tin/{STATE}/{WORKUNIT}"
    DSM_DIR = f"{DATA_DIR}/dsm/{STATE}/{WORKUNIT}"
    INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
    INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_{CRS}.gpkg"

    for d in [DATA_DIR, PC_DIR, BCM_DIR, TIN_DIR, DSM_DIR, INDEX_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()