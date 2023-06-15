import csv
import numpy as np


def read_csv_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = [row for row in reader]
    return np.array(data, dtype=float)


data = read_csv_data('raw_data.csv')

# Create unique nodes using the [0, 1] coordinate pairs
nodes = np.unique(data[:, [0, 1]], axis=0)

# Go through each row's [2, 3] coordinate pair, if it is not in nodes list, add it
for row in data:
    additional_node = row[[2, 3]]
    if not any(np.array_equal(additional_node, node) for node in nodes):
        nodes = np.concatenate((nodes, additional_node.reshape(1, -1)))

# Write unique nodes to file
with open('nodes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(nodes)

# Create a dictionary to map nodes to indices
node_to_index = {tuple(node): idx for idx, node in enumerate(nodes)}

# Prepare edge data with indices
edges = []
for row in data:
    node1 = tuple(row[[0, 1]])
    node2 = tuple(row[[2, 3]])
    weight = row[4]

    edges.append([node_to_index[node1], node_to_index[node2], weight])

# Write edge data to file
with open('edges.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(edges)
