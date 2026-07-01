import pandas as pd

results = pd.read_csv("data/results.csv")
situas = pd.read_csv("data/situas.csv", sep=";", decimal=",")

situas = situas[["Codice Comune (numerico)", "Comune", "Sigla automobilistica", "Codice Regione"]].rename(columns={
    "Codice Comune (numerico)": "municipality_code",
    "Comune": "municipality_name",
    "Sigla automobilistica": "province_code",
    "Codice Regione": "region_code"
})

df = results.merge(situas, on="municipality_code", how="left")
df = df.drop(columns=["cluster"])

df["acc_per_capita"] = df["acc_per_capita"].round(6)
df["acc_per_kmq"] = df["acc_per_kmq"].round(6)
    

df.to_csv("data/powerbi_export.csv", index=False)
print(df.columns.tolist())
print(df.shape)

