import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns 

df = pd.read_csv("data/merged.csv")
df = df.dropna(subset=["acc_per_capita", "acc_per_kmq"])

X = df[["acc_per_capita", "acc_per_kmq"]]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

k_values = (range(1, 10))
wcss_list = []
for k in k_values:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    wcss_list.append(km.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(k_values, wcss_list, marker="o")
plt.title("Within Cluster Sum of Squares - by k")
plt.xlabel("k")
plt.ylabel("WCSS Score")
plt.tight_layout()
plt.savefig("figures/elbow_kmeans.png", dpi=150)
plt.show()

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

cluster_means = df.groupby("cluster")[["acc_per_capita", "acc_per_kmq"]].mean()
print(cluster_means)

order = cluster_means["acc_per_capita"].sort_values().index.tolist()
cluster_labels = {order[0]: "low", order[1]: "medium", order[2]: "high"}
df["risk_tier"] = df["cluster"].map(cluster_labels)

perm = df[df["risk_tier"].isin(["low", "high"])][["risk_tier", "acc_per_capita"]].reset_index(drop=True)

mu_high = np.mean(perm[perm["risk_tier"] == "high"]["acc_per_capita"])
mu_low = np.mean(perm[perm["risk_tier"] == "low"]["acc_per_capita"])
mu_diff = mu_high - mu_low
print("Observed test statistic (mean high - mean low):", round(mu_diff, 6)) 

n = 2000
np.random.seed(1)
mu_diff_samples = []
for i in range(n):
    df_sample1 = perm.sample(frac=0.5, replace=False)
    ix2 = set(perm.index) - set(df_sample1.index)
    df_sample2 = perm.loc[list(ix2)]
    mu_diff_temp = np.mean(df_sample1["acc_per_capita"]) - np.mean(df_sample2["acc_per_capita"])
    mu_diff_samples.append(mu_diff_temp)

sns.histplot(mu_diff_samples)
plt.axvline(mu_diff, 0, 1, color="r", linestyle="--")
plt.title("Permutation distribution of the difference in means")
plt.tight_layout()
plt.savefig("figures/permutation_test.png", dpi=150)
plt.show()

p_value = sum([el >= mu_diff for el in mu_diff_samples]) / n
print("Values as extreme as observed:", sum([el >= mu_diff for el in mu_diff_samples]))
print("p-value:", p_value)

alpha = 0.05
if p_value <= alpha:
    print("p-value <= alpha | statistically significant | H0 rejected")
else:
    print("p-value > alpha | not statistically significant | H0 accepted")

df.to_csv("data/results.csv", index=False)
print("saved")