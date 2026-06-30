import pandas as pd

df = pd.read_csv("data/raw_istat.csv", low_memory=False)

df = df[df["TIPO_DATO"] == "ROADACC"]
df = df[["ITTER107", "TIME_PERIOD", "OBS_VALUE"]]
df = df.rename(columns={
    "ITTER107": "municipality_code",
    "TIME_PERIOD": "year",
    "OBS_VALUE": "accidents"
})

df["year"] = pd.to_datetime(df["year"]).dt.year

df.to_csv("data/clean_istat.csv", index=False)
print("saved")