import geopandas as gp
from osgeo import gdal
import os
import boto3
import rasterio as rio

# python3 compute-local-solar.py

def main():
    s3 = get_creds()
    
    # Download files
    for f in [SOLAR, ADDY]:
        if not os.path.exists(f):
            s3.download_file(BUCKET, f, f)
            
    addy = gp.read_file(ADDY)
    
    df = []
    for index, row in addy.iterrows():
        clip_tif = os.path.join(SOLAR_DIR, f"{row.address_id}.tif")
        buff_geom = row['geometry'].buffer(BUFFER)
        minx, miny, maxx, maxy = buff_geom.bounds
        
        gdal.Translate(
            clip_tif,
            SOLAR,
            projWin=[minx, maxy, maxx, miny],
            outputBounds=[minx, maxy, maxx, miny],
            stats=True,
            callback=gdal.TermProgress_nocb
        )
        
        # tif = rio.open(clip_tif)
        # tif_arry = tif.read()
        # mean_val = tif_arry.mean()
        
        tif = gdal.Open(clip_tif)
        tif_band = tif.GetRasterBand(1)
        stats = tif_band.GetStatistics( True, True )
        mean_val = stats[2]
        print(mean_val)
        
        if mean_val != 'inf':
            row['solar_watts_mean'] = round(mean_val, 2)
        else:
            row['solar_watts_mean'] = 'NA'
        
        df.append(row)
        
        #os.remove(clip_tif)
        
        if index >= 10:
            break
        
        
    # solar_addy = os.path.join(SOLAR_DIR, f"{os.path.basename(ADDY).split('.')[0]}-solar-average.gpkg")
    # gp.GeoDataFrame(df, crs=addy.crs).to_file(solar_addy, driver='GPKG')
    
    # s3.upload_file(solar_addy, BUCKET, solar_addy)
    
def get_creds():
    s3 = boto3.client(
        's3',
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    return s3 
    
if __name__ == "__main__":
    BUCKET = "health-hub-analysis"
    SOLAR_DIR = os.path.join("data", "palm-north", "solar")
    CLIPS_DIR = os.path.join('data', 'palm-north', 'vector-clips')
    
    SOLAR = os.path.join(SOLAR_DIR, "solar-average-merged.tif")
    ADDY = os.path.join(CLIPS_DIR, "nz-addresses.gpkg")
    
    BUFFER = 25
    
    for d in [SOLAR_DIR, CLIPS_DIR]:
        os.makedirs(d, exist_ok=True)
    
    main()