#!/usr/bin/env python
import os
import sys
from py_utils import *
from globals import *


def main():
    s3 = get_creds()    
    get_s3_file(s3, IN_FILE, WESM_SURFACE_BUCKET)
    dsm_file = f"{DSM_DIR}/{BASENAME}.tif"   

    metadata = get_pc_metadata(IN_FILE)    

    print("Making DSM...")
    make_dsm(PIPELINE_DSM, IN_FILE, metadata.wkt, dsm_file, metadata.bounds)
     
    
if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    BASENAME = os.path.basename(IN_FILE).split('.')[0]

    for d in [DATA_DIR, BCM_DIR, DSM_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()