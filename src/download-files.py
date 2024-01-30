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
    
    with open(LIST_FILE) as f:
        list = f.readlines() 

    for l in list:
        index_row = index_file[index_file['file_name'] == os.path.basename(l.strip())]
        local_pc = f"{PC_DIR}/{l.strip()}"
        try: 
            if not os.path.exists(local_pc):
                s3.download_file(USGS_BUCKET, index_row.usgs_loc.values[0], local_pc, ExtraArgs={'RequestPayer':'requester'})
        except:
            print("File Not Found")

if __name__ == "__main__":
    
    for d in [DATA_DIR, PC_DIR, BCM_DIR, TIN_DIR, DSM_DIR, INDEX_DIR, LIST_PATH]:
        os.makedirs(d, exist_ok=True)

    main()