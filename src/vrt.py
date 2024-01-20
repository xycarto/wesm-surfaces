#!/usr/bin/env python
import os
import sys
from py_utils import *
from globals import *


def main():
    s3 = get_creds()    
    
    # if os.path.basename(IN_DIR) == "hillshade":
    #     vrt_dir = os.path.join(VRT_DIR, "hillshade")
    #     in_dir = IN_DIR.split("/")[0]
    #     vrt = os.path.join(vrt_dir, f"{in_dir}-hillshade.vrt")
    #     build_vrt(vrt_dir, vrt)
    # else:
    #     vrt = os.path.join(VRT_DIR, f"{IN_DIR}.vrt")
    #     build_vrt(VRT_DIR, vrt)

    vrt = os.path.join(VRT_DIR, f"{PROCESS}.vrt")
    build_vrt(VRT_DIR, vrt)
             
    print(f"Uploading {vrt}...")
    s3.upload_file(vrt, WESM_SURFACE_BUCKET, vrt)


if __name__ == "__main__":
    VRT_DIR = f"{DATA_DIR}/{PROCESS}/{STATE}/{WORKUNIT}"

    for d in [DATA_DIR]:
        os.makedirs(d, exist_ok=True)

    main()