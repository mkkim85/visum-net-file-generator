import pandas as pd
import numpy as np
from tqdm import tqdm_notebook

df_od = pd.read_csv('input/od.csv')

date = '2019-09-02'
od_data = df_od[(df_od['승차일시'] == date)]
bus_stops = set(od_data['승차정류장ID'])
df_od_matrix = pd.DataFrame(index=bus_stops, columns=bus_stops)

for i, row in tqdm_notebook(od_data.iterrows(), total=len(od_data)):
    df_od_matrix.loc[[row['승차정류장ID']], [row['승차정류장ID']]] = row['이용객수']

df_od_matrix.to_csv('output/od_matrix.csv', index=True, encoding='utf-8-sig')