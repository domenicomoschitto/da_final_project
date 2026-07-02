import pandas as pd

df = pd.read_csv("data/clean_istat.csv")

df_situas = pd.read_csv("data/situas.csv", sep=";", decimal=",")
df_situas = df_situas[["Codice Comune (numerico)", "Popolazione residente", "Superficie (Kmq)"]]
df_situas.columns = ["municipality_code", "population", "area_kmq"]
df_situas["area_kmq"] = pd.to_numeric(df_situas["area_kmq"].str.replace(",", "."), errors="coerce")

df_merged = df.merge(df_situas, on="municipality_code", how="inner")
df_merged["acc_per_capita"] = df_merged["accidents"] / df_merged["population"]
df_merged["acc_per_kmq"] = df_merged["accidents"] / df_merged["area_kmq"]

print(df_merged.head())
df_merged.to_csv("data/merged.csv", index=False)
print("saved")