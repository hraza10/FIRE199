import csv
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import distance


def read_csv_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = [row for row in reader]
    return np.array(data, dtype=float)


def merge_close_nodes(nodes, edges, eps):
    db = DBSCAN(eps=eps, min_samples=1).fit(nodes)
    labels = db.labels_

    # average out the nodes in the same cluster
    new_nodes = []
    for label in set(labels):
        new_nodes.append(np.mean(nodes[labels == label], axis=0))

    # update the edges to reflect the merged nodes
    new_edges = []
    for edge in edges:
        new_edge = edge.copy()
        for i, node in enumerate(nodes):
            if distance.euclidean(new_edge[:2], node) <= eps:
                new_edge[:2] = new_nodes[labels[i]][:2]
            if distance.euclidean(new_edge[2:4], node) <= eps:
                new_edge[2:4] = new_nodes[labels[i]][:2]
        new_edges.append(new_edge)

    return np.array(new_nodes), new_edges


data = read_csv_data('raw_data.csv')

# Create unique nodes using the [0, 1] and [2, 3] coordinate pairs
nodes = np.vstack((data[:, [0, 1]], data[:, [2, 3]]))
edges = data.tolist()

# Merge nodes that are too close
eps = 0.00008
nodes, edges = merge_close_nodes(nodes, edges, eps)

# Create a dictionary to map nodes to indices
node_to_index = {tuple(node): idx for idx, node in enumerate(nodes)}

# Prepare edge data with indices
new_edges = []
for edge in edges:
    node1 = tuple(edge[:2])
    node2 = tuple(edge[2:4])
    weight = edge[4]

    new_edges.append([node_to_index[node1], node_to_index[node2], weight])

# Write edge data to file
with open('edges.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_edges)

# Write unique nodes to file
with open('nodes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(nodes)
