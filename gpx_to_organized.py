import csv
import gpxpy
import numpy as np
import os 
import pandas as pd
from sklearn.cluster import DBSCAN
from scipy.spatial import distance

folder_path = 'gpx_files'
csv_folder = 'csv_files' 
raw_folder = 'raw_data_files'

# Gets a list of all files in gpx_files
gpx_list = os.listdir(folder_path)

# Convert date string to datetime object
def convert_to_datetime(t):
    return pd.to_datetime(t, format='%Y-%m-%d %H:%M:%S%z')

def gpx_to_csv(gpx_file, csv_file): 
    # Opens GPX file
    f = open(gpx_file, 'r')
    
    gpx = gpxpy.parse(f)
        
    # Opens CSV file for writing
    with open(csv_file, 'w', newline='') as f: 
        csv_writer = csv.writer(f) 
        
        # Writes the header row
        csv_writer.writerow(['Latitude', 'Longitude', 'Time']) 
        
        # Iterates over each track in the GPX file
        for track in gpx.tracks:
            # Iterates over each segment
            for segment in track.segments:
                #Iterates over each point
                for point in segment.points:
                    csv_writer.writerow([point.latitude, point.longitude, point.time])
                    
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

# Converts CSV file to numpy array. 
def read_csv_data(file_path): 
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter = ',')
        data = [row for row in reader]
    return np.array(data, dtype=float)


# Calculate the time difference in seconds
def time_difference(t1, t2):
    return (t2 - t1).total_seconds()

                    
# Iterates over each of the files.
for file_name in gpx_list:
    file_path = os.path.join(folder_path, file_name)
    # Checks for file directories.
    if (os.path.isfile(file_path)): 
        # Converts each of the gpx files to csv files.
        gpx_name = os.path.splitext(os.path.basename(file_path))[0]
        csv_name = os.path.join(csv_folder, gpx_name + '.csv')
        gpx_to_csv(file_path, csv_name)

        data = []
        with open(csv_name, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header
            for row in reader:
                # Add the datetime object and float coordinates to the data list
                data.append([float(row[0]), float(row[1]), convert_to_datetime(row[2])])

        # Convert the list to a numpy array
        data = np.array(data, dtype=object)

        # Prepare output data
        output = []
        for i in range(1, len(data)):
            output.append([
            "{:.10f}".format(data[i - 1, 1]),  # Coordinate 1 lat
            "{:.10f}".format(data[i - 1, 0]),  # Coordinate 1 long
            "{:.10f}".format(data[i, 1]),      # Coordinate 2 lat
            "{:.10f}".format(data[i, 0]),      # Coordinate 2 long
            time_difference(data[i - 1, 2], data[i, 2])  # Time difference
            ])

            
# Convert the output list to a numpy array
output = np.array(output)

# Append output to CSV file
with open('raw_data.csv', 'a', newline='') as f:
    np.savetxt(f, output, delimiter=",", fmt='%s')

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
