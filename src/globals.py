import os 

DATA_DIR = os.environ.get("DATA_DIR")
WORKUNIT = os.environ.get("WORKUNIT") 
STATE = os.environ.get("STATE")
TYPE = os.environ.get("TYPE")
PROCESS = os.environ.get("PROCESS")

## CONSTANTS
USGS_BUCKET = "usgs-lidar"
WESM_SURFACE_BUCKET = "xyc-wesm-surfaces"
WESM_GRID_BUCKET = "xyc-wesm-grids"
WESM_VIEWER_BUCKET = "xyc-wesm-viewer"
BCM_BUFFER = 50
CRS = "4269"
TEST_NUM = 10
PC_DIR = f"{DATA_DIR}/point-clouds/{STATE}/{WORKUNIT}"
BCM_DIR = f"{DATA_DIR}/bcm/{STATE}/{WORKUNIT}"    
TIN_DIR = f"{DATA_DIR}/tin/{STATE}/{WORKUNIT}"         
DSM_DIR = f"{DATA_DIR}/dsm/{STATE}/{WORKUNIT}"      
#CLIP_DIR = f"{DATA_DIR}/clips/{os.path.basename(IN_FILE).split('.')[0]}"
INDEX_DIR = f"{DATA_DIR}/index-indv/{STATE}"
GRID_INDEX_DIR = f"data/index-indv/{STATE}"
INDEX_FILE = f"{INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"
GRID_INDEX_FILE = f"{GRID_INDEX_DIR}/{WORKUNIT}_index_4269.gpkg"

PIPELINE_CROP_FILTER = 'src/pipeline-templates/buffer-clip-filter-template.json'
PIPELINE_DSM = 'src/pipeline-templates/dsm_template.json'
PIPELINE_TIN = 'src/pipeline-templates/tin_template.json'

