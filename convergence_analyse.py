import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("weights_log.csv")

gen_weights = df.groupby("generation")[["w0", "w1", "w2", "w3"]].mean()

plt.figure(figsize=(10, 6))

for w in ["w0", "w1", "w2", "w3"]:
    plt.plot(gen_weights.index, gen_weights[w], label=w)

plt.xlabel("Generation")
plt.ylabel("Weight Value")
plt.title("Evolution of Each Weight Over Generations")
plt.legend()
plt.grid(True)
plt.show()
