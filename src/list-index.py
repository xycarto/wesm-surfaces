import os
import geopandas as gp
import sys
from py_utils import *
from globals import *

# python3 process/list-index.py "CA_SantaClaraCounty_2020"

# set AWS credentials

def main():  

    s3 = get_creds()
    get_grid_index(s3, WESM_GRID_BUCKET, GRID_INDEX_FILE, INDEX_FILE)
    index_file = gp.read_file(INDEX_FILE)

    if os.path.exists(LIST_FILE):
        os.remove(LIST_FILE)

    with open(LIST_FILE,'w') as grid_list:
        if TEST_NUM == 0:
            for index, row in index_file.iterrows():
                grid_list.write(f"{row.file_name}\n")
        else:
            for index, row in index_file.iterrows():
                grid_list.write(f"{row.file_name}\n")
                if index >= TEST_NUM:
                    exit()
            
if __name__ == "__main__":

    TEST_NUM = int(sys.argv[1]) # USE input 0 for all

    for d in (LIST_PATH, INDEX_DIR):
        os.makedirs(d, exist_ok=True)
        
    main()
