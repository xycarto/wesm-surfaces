import boto3
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gp
import sys
from py_utils import *
from globals import *

# Example: time make download-files workunit=CA_NoCAL_Wildfires_B1_2018 state=California process=bcm type=test location=local 

def main():    
    s3 = get_creds()
    get_grid_index(s3, WESM_GRID_BUCKET, GRID_INDEX_FILE, INDEX_FILE)

    # Read in Index
    index_file = gp.read_file(INDEX_FILE)

    # Parse Index
    for i, row in index_file.iterrows():
        bucket, in_file, local_file = set_paths(row)
        print(f"Downloading {local_file}")
        try: 
            if not os.path.exists(local_file):
                s3.download_file(bucket, in_file, local_file, ExtraArgs={'RequestPayer':'requester'})
        except:
            print("File Not Found")
        if TYPE == "test":
            if i >= TEST_NUM:
                exit()

def set_paths(row):
    if PROCESS == "bcm":
        bucket = USGS_BUCKET
        in_file = row.usgs_loc
        local_file= os.path.join(PC_DIR, row.file_name)
    elif PROCESS == "dsm" or PROCESS == "tin":
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
    
    for d in [DATA_DIR, PC_DIR, BCM_DIR, TIN_DIR, DSM_DIR, INDEX_DIR]:
        os.makedirs(d, exist_ok=True)

    main()