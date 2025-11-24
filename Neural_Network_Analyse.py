import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("weights_log.csv")

# Aggregate by generation
heatmap_data = df.groupby("generation").agg({
    "w0": "mean",
    "w1": "mean",
    "w2": "mean",
    "w3": "mean"
})


plt.figure(figsize=(8,6))
sns.heatmap(heatmap_data.T, annot=True ,  cmap="coolwarm", cbar_kws={'label': 'Weight Value'} ) # fmt=".4f")
plt.xlabel("Generation")
plt.ylabel("Weights")
plt.title("Evolution of Neural Network Weights")
plt.show()

