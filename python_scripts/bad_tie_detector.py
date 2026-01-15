import random

import geopandas as gpd
import rioxarray
from shapely import Point


def lambda_handler(event, context = None):

    flight = event['flight']
    image_index = event['image_index']
    if random.random() < .01:
        
        mask_file = "s3://dw-trackview/{}/raster/mask_{}.cog".format(flight, image_index)
        
        data = rioxarray.open_rasterio(mask_file)
        x_centroid = data.coords['x'].mean()
        y_centroid = data.coords['y'].mean()
        
        df_out = gpd.GeoDataFrame({'name': ['suspected_bad_ties'], 'flight': [flight], 'image_index': [image_index]})\
            .set_geometry([Point(x_centroid, y_centroid)])\
            .set_crs('epsg:4326')
        
        outfile = "s3://dw-trackview/{}/annotations/bad_ties_{}.parquet".format(flight, image_index)
        df_out.to_parquet(outfile)




if __name__ == '__main__':

    event = {
        "flight": "demo_20250815_demo_cando_rail_demo_flight_1d7d91e1",
        "image_index": 5
    }
    lambda_handler(event)