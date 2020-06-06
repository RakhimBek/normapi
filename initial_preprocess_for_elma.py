import pandas as pd
import numpy as np

good = pd.read_csv('good.csv', sep=';', header=None,  error_bad_lines=False , dtype=str)

cols = good.iloc[0:,3:]
cols = cols.replace(np.nan, '', regex=True)
cols =cols.astype(str)
cols = cols.apply(','.join, axis=1)


dropped = good.drop(columns=[2,3,4,5,6,7,8,9,10,11,12,13,14,15])
dropped['after'] = cols
dropped.to_csv('after.csv')

