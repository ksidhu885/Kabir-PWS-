import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("network_log.csv")


df = df.sort_values("generation")


connections_per_gen = df.groupby("generation").size()


def count_unique_nodes(group):
    from_nodes = group["from_node_id"].unique()
    to_nodes = group["to_node_id"].unique()
    all_nodes = set(from_nodes) | set(to_nodes)
    return len(all_nodes)

nodes_per_gen = df.groupby("generation").apply(count_unique_nodes)

plt.figure(figsize=(10, 5))
plt.plot(connections_per_gen.index, connections_per_gen.values, marker="o")
plt.xlabel("Generation")
plt.ylabel("Number of Connections")
plt.title("Network Complexity: Connections per Generation")
plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(nodes_per_gen.index, nodes_per_gen.values, marker="o")
plt.xlabel("Generation")
plt.ylabel("Number of Unique Nodes")
plt.title("Network Complexity: Nodes per Generation")
plt.grid(True)
plt.tight_layout()
plt.show()

