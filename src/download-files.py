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
        print(f"Downloading {local_file} from bucket: {bucket}")
        try: 
            if not os.path.exists(local_file):
                s3.download_file(bucket, in_file, local_file, ExtraArgs={'RequestPayer':'requester'})
        except:
            print("File Not Found")
        if TYPE == "test":
            if i >= TEST_NUM:
                exit()

def set_paths(row):
    basename = os.path.basename(row.file_name).split('.')[0]
    if PROCESS == "bcm":
        bucket = USGS_BUCKET
        in_file = row.usgs_loc
        local_file= os.path.join(PC_DIR, row.file_name)
    elif (PROCESS == "dsm" or PROCESS == "tin") and COG == "false":
        bucket = WESM_SURFACE_BUCKET
        if HS == "true" and PROCESS == "dsm":
            in_file = f"{DSM_DIR}/{basename}.tif"
        elif HS == "true" and PROCESS == "tin":
            in_file = f"{TIN_DIR}/{basename}.tif"
        else:
            in_file = f"{BCM_DIR}/{row.file_name}"
        local_file = in_file
    elif PROCESS == "solar" and COG == 'false':
        bucket = WESM_SURFACE_BUCKET
        in_file = f"{DSM_DIR}/{basename}.tif"
        local_file = in_file
    elif COG == "true":
        bucket = WESM_SURFACE_BUCKET
        if HS == "true" and PROCESS == "dsm":
            in_file = f"{DSM_DIR}/hillshade/{basename}.tif"
        elif HS == "true" and PROCESS == "tin":
            in_file = f"{TIN_DIR}/hillshade/{basename}.tif"
        else:
            in_file = f"{DATA_DIR}/{PROCESS}/{STATE}/{WORKUNIT}/{basename}.tif"        
        local_file = in_file        
    else:
        print("Unknown input...")
    
    return bucket, in_file, local_file

if __name__ == "__main__":
    
    for d in [DATA_DIR, PC_DIR, BCM_DIR, TIN_DIR, DSM_DIR, INDEX_DIR]:
        os.makedirs(d, exist_ok=True)

    main()