import pandas as pd

results = pd.read_csv("data/results.csv")
merged = pd.read_csv("data/merged.csv")

situas = pd.read_csv("data/situas.csv", sep=";", decimal=",")
situas = situas[["Codice Comune (numerico)", "Comune", "Sigla automobilistica", "Codice Regione"]].rename(columns={
    "Codice Comune (numerico)": "municipality_code",
    "Comune": "municipality_name",
    "Sigla automobilistica": "province_code",
    "Codice Regione": "region_code"
})

comuni = pd.read_csv("data/comuni_istat.csv", sep=";", encoding="latin1")
comuni = comuni[[
    "Codice Comune formato numerico",
    "Denominazione Regione",
    "Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)"
]].rename(columns={
    "Codice Comune formato numerico": "municipality_code",
    "Denominazione Regione": "region_name",
    "Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)": "province_name"
}).drop_duplicates(subset="municipality_code")

totals = results.merge(situas, on="municipality_code", how="left")
totals = totals.merge(comuni, on="municipality_code", how="left")
totals = totals.drop(columns=["cluster"])
totals["acc_per_capita"] = totals["acc_per_capita"].round(6)
totals["acc_per_kmq"] = totals["acc_per_kmq"].round(6)

totals.to_csv("data/powerbi_export.csv", index=False)

yearly = merged[["municipality_code", "year", "accidents", "acc_per_capita", "acc_per_kmq"]]
yearly = yearly.merge(results[["municipality_code", "risk_tier"]], on="municipality_code", how="left")
yearly = yearly.merge(situas[["municipality_code", "municipality_name", "province_code", "region_code"]], on="municipality_code", how="left")
yearly = yearly.merge(comuni, on="municipality_code", how="left")
yearly["acc_per_capita"] = yearly["acc_per_capita"].round(6)
yearly["acc_per_kmq"] = yearly["acc_per_kmq"].round(6)
yearly.to_csv("data/powerbi_yearly.csv", index=False)

print("powerbi_export:", totals.shape)
print("powerbi_yearly:", yearly.shape)
print("totals columns:", totals.columns.tolist())