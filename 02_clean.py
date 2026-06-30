import pandas as pd

df = pd.read_csv("data/raw_istat.csv", low_memory=False)
print(df.shape)

df = df[df["TIPO_DATO"] == "ROADACC"]
print(df.shape)

df = df[["ITTER107", "TIME_PERIOD", "OBS_VALUE"]]
print(df.shape)

df = df.rename(columns={
    "ITTER107": "municipality_code",
    "TIME_PERIOD": "year",
    "OBS_VALUE": "accidents"
})
print(df.columns.tolist())

df["year"] = pd.to_datetime(df["year"]).dt.year
print(df["year"].unique())

df.to_csv("data/clean_istat.csv", index=False)
print("saved")