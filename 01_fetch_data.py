import pandas as pd
from istatapi import discovery, retrieval

ds = discovery.DataSet("41_983")
ds.dimensions

data = retrieval.get_data(ds)
df = pd.DataFrame(data)

df.to_csv("data/raw_istat.csv", index=False)

print(df.shape)
print(df.columns.tolist())
print(df.head(10))
print(df["TIPO_DATO"].value_counts())