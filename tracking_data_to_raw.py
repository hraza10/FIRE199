import csv
import numpy as np
import pandas as pd


# Convert date string to datetime object
def convert_to_datetime(t):
    return pd.to_datetime(t, format='%Y/%m/%d %H:%M:%S%z')


# Calculate the time difference in seconds
def time_difference(t1, t2):
    return (t2 - t1).total_seconds()


data = []
with open('Xfinity-eppley_-GPX-20230615121358.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        # Add the datetime object and float coordinates to the data list
        data.append([float(row[0]), float(row[1]), convert_to_datetime(row[6])])

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
