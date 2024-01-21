#!/usr/bin/env python
import os
import sys
from py_utils import *
from globals import *


def main():
    s3 = get_creds()    
    
    if HS == "true":
        vrt_dir = f"{VRT_DIR}/hillshade"
        vrt = f"{vrt_dir}/{PROCESS}-hs.vrt"
    else:
        vrt_dir = VRT_DIR
        vrt = f"{VRT_DIR}/{PROCESS}.vrt"

    build_vrt(vrt_dir, vrt)
             
    print(f"Uploading {vrt}...")
    s3.upload_file(vrt, WESM_SURFACE_BUCKET, vrt)


if __name__ == "__main__":
    VRT_DIR = f"{DATA_DIR}/{PROCESS}/{STATE}/{WORKUNIT}"

    for d in [DATA_DIR]:
        os.makedirs(d, exist_ok=True)

    main()