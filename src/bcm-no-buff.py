#!/usr/bin/env python
import os
import geopandas as gp
import sys
from py_utils import *
from globals import *


def main():
    s3 = get_creds()
    get_grid_index(s3, WESM_GRID_BUCKET, GRID_INDEX_FILE, INDEX_FILE)

    index_file = gp.read_file(INDEX_FILE)
    index_row = index_file[index_file['file_name'] == os.path.basename(IN_FILE)]

    get_usgs_file(s3, index_row.usgs_loc.values[0], IN_FILE, USGS_BUCKET)

    filter_laz(IN_FILE, index_row)    

if __name__ == "__main__":

    IN_FILE = sys.argv[1]
        
    for d in [DATA_DIR, PC_DIR, BCM_DIR,INDEX_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()