import os 

## Environment vars from: configs/process-config.env
DATA_DIR = os.environ.get("DATA_DIR")
WORKUNIT = os.environ.get("WORKUNIT") 
STATE = os.environ.get("STATE")
TYPE = os.environ.get("TYPE")
PROCESS = os.environ.get("PROCESS")
TEST_NUM = int(os.environ.get("TEST_NUM"))
HS = os.environ.get("HS")
COG = os.environ.get("COG")

## CONSTANTS
USGS_BUCKET = "usgs-lidar"
WESM_SURFACE_BUCKET = "xyc-wesm-surfaces"
WESM_GRID_BUCKET = "xyc-wesm-grids"
WESM_VIEWER_BUCKET = "xyc-wesm-viewer"
BCM_BUFFER = 50
CRS = "4269"
RESOLUTION = 1

## DIRS and Files
PC_DIR = f"{DATA_DIR}/point-clouds/{STATE}/{WORKUNIT}"
BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}"    
TIN_DIR = f"{DATA_DIR}/tin/{STATE}/{WORKUNIT}"         
DSM_DIR = f"{DATA_DIR}/dsm/{STATE}/{WORKUNIT}"   
SOLAR_DIR = f"{DATA_DIR}/solar/{STATE}/{WORKUNIT}"
COG_DIR = f"{DATA_DIR}/cog/{STATE}/{WORKUNIT}"
INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
GRID_INDEX_DIR = f"data/index-indv/{STATE}"
INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"
GRID_INDEX_FILE = f"{GRID_INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"

## PDAL Pipelines
PIPELINE_CROP_FILTER = 'src/pipeline-templates/buffer-clip-filter-template.json'
PIPELINE_FILTER = 'src/pipeline-templates/buffer-clip-filter-template-filter-only.json'
PIPELINE_DSM = 'src/pipeline-templates/dsm_template.json'
PIPELINE_TIN = 'src/pipeline-templates/tin-template.json'

