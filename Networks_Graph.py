import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("weights_log.csv")


best_scores = df.groupby("generation")["score"].max()

plt.figure(figsize=(10,6))
plt.plot(best_scores.index, best_scores.values, marker="o")

plt.title("Learning Curve: Best Score per Generation")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.grid(True)
plt.tight_layout()
plt.show()
