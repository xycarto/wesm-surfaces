#!/usr/bin/env python
import os
import boto3
import sys
import subprocess as sub
from py_utils import *
from globals import *


def main():
    s3 = get_creds()    

    out_hs = f"{HS_DIR}/{os.path.basename(IN_FILE)}"  
    sub.call(
        f"gdaldem hillshade -compute_edges {IN_FILE} {out_hs}",
        shell=True
    )
    
    print(f"Uploading {out_hs}...")
    # s3.upload_file(out_hs, WESM_SURFACE_BUCKET, out_hs)


if __name__ == "__main__":
    IN_FILE = sys.argv[1]
    SURFACE_DIR = f"{DATA_DIR}/{PROCESS}/{STATE}/{WORKUNIT}"
    HS_DIR = f"{SURFACE_DIR}/hillshade"

    for d in [DATA_DIR, SURFACE_DIR, HS_DIR]:
        os.makedirs(d, exist_ok=True)

    main()