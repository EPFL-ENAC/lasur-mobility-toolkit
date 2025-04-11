import pandas as pd
import geopandas as gpd
import os
from pathlib import Path

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
dest_dir = os.path.join(os.path.dirname(__file__), '..', 'typo_modal', 'data')

print(f'Converting data from {data_dir} to {dest_dir}...')

pathlist = Path(data_dir).glob('**/*.csv')
for path in pathlist:
    path_csv = str(path)
    path_parquet = path_csv.replace('.csv', '.parquet').replace(data_dir, dest_dir)
    print(f'Converting {path_csv} to {path_parquet}')
    df = pd.read_csv(path_csv)
    df.to_parquet(path_parquet)
    print(f'Conversion done.')

pathlist = Path(data_dir).glob('**/*.shp')
for path in pathlist:
    path_shp = str(path)
    path_parquet = path_shp.replace('.shp', '.parquet').replace(data_dir, dest_dir)
    print(f'Converting {path_shp} to {path_parquet}')
    df = gpd.read_file(path_shp)
    df.to_parquet(path_parquet)
    print(f'Conversion done.')
