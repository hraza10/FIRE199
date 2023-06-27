""" This version uses a different formatting when converting the date string to a date time object. """
import csv
import gpxpy
import numpy as np
import os 
import pandas as pd

folder_path = 'gpx_files'
csv_folder = 'csv_files' 
raw_folder = 'raw_data_files'

# Gets a list of all files in gpx_files
gpx_list = os.listdir(folder_path)

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
                    csv_writer.writerow([point.latitude, point.latitude, point.time])
                    
                    
def read_csv_data(file_path): 
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter = ',')
        data = [row for row in reader]
    return np.array(data, dtype=float)



# Convert date string to datetime object
def convert_to_datetime(t):
    return pd.to_datetime(t, format='%Y-%m-%d %H:%M:%S%z')


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
                print(row[2])
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
