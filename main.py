import csv
from math import asin, cos, sqrt, radians
import webbrowser
import numpy as np
import geopandas as gpd
import folium
from scipy.sparse.csgraph import shortest_path
from scipy.sparse import csr_matrix
import sys

origin = [38.98691761313879, -76.94256431247602]  # (0, 0)


def read_csv_data(file_path):
    data = np.genfromtxt(file_path, delimiter=',')
    return data


edges = read_csv_data('edges.csv')
rows = edges[:, 0]
cols = edges[:, 1]
data = edges[:, 2]
max_id = int(np.max(edges[:, :2]))
adjacency_matrix = csr_matrix((data, (rows, cols)), shape=(max_id + 1, max_id + 1))

# To find the shortest path between all nodes
dist_matrix, predecessors = shortest_path(csgraph=adjacency_matrix, directed=False, return_predecessors=True)


def plot_all_data_on_map(file_path):
    data = read_csv_data(file_path)

    # Create a GeoDataFrame from the data
    gdf = gpd.GeoDataFrame(
        {'id': range(len(data))},
        geometry=gpd.points_from_xy(data[:, 1], data[:, 0]),  # Swapped longitude and latitude
        crs="EPSG:4326"  # this is the coordinate system for GPS
    )

    # Create a folium map centered at the mean of the coordinates
    m = folium.Map(location=[data[:, 0].mean(), data[:, 1].mean()], zoom_start=13)  # Swapped longitude and latitude

    # Add all points to the map
    for _, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3,  # Adjust as needed
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.6  # Adjust as needed
        ).add_to(m)

    # Draw all edges between the nodes
    draw_edges_on_map(m, gdf, edges)

    return m


def draw_edges_on_map(m, gdf, edges):
    for edge in edges:
        start_node = gdf.loc[int(edge[0]), 'geometry']
        end_node = gdf.loc[int(edge[1]), 'geometry']
        folium.PolyLine([(start_node.y, start_node.x), (end_node.y, end_node.x)], color='black').add_to(m)


# Function to construct path from predecessors matrix
def construct_path(start, end, predecessors):
    path = []
    i = end
    while i != start:
        path.append(i)
        i = predecessors[start, i]
    path.append(start)
    path.reverse()
    return path


def draw_optimal_route(file_path, start, end, predecessors):
    # Check if there is a path between start and end
    if predecessors[start, end] == -9999:
        print(f"No path exists between node {start} and node {end}.")
        sys.exit();

    data = read_csv_data(file_path)

    # Construct the path
    path = construct_path(start, end, predecessors)

    print(f"The computed path is: {path}")

    # Create a GeoDataFrame from the data of nodes in the path
    gdf = gpd.GeoDataFrame(
        {'id': path},
        geometry=gpd.points_from_xy(data[path, 1], data[path, 0]),  # Swapped longitude and latitude
        crs="EPSG:4326"  # this is the coordinate system for GPS
    )

    # Create a folium map centered at the mean of the coordinates in the path
    m = folium.Map(location=[data[path, 0].mean(), data[path, 1].mean()],
                   zoom_start=13)  # Swapped longitude and latitude

    # Add the points in the path to the map
    for _, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3,  # Adjust as needed
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6  # Adjust as needed
        ).add_to(m)

    # Add the lines in the path to the map
    for i in range(len(path) - 1):
        start_node = gdf.iloc[i]['geometry']
        end_node = gdf.iloc[i + 1]['geometry']
        folium.PolyLine([(start_node.y, start_node.x), (end_node.y, end_node.x)], color='green').add_to(m)

    return m


# calculates distance between two sets of longitude and latitude
def distance(lat1, lon1, lat2, lon2):
    # approximate radius of Earth in km
    R = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # haversine formula to calculate distance
    hav = 0.5 - cos(lat2_rad - lat1_rad) / 2 + cos(lat1_rad) * cos(lat2_rad) * (1 - cos(lon2_rad - lon1_rad)) / 2
    return (2 * R) * asin(sqrt(hav))


# uses distance function to find nearest pair of longitude and latitude in a given file to a given pair
def nearest(csv_file, given_lat, given_lon):
    nearest_dist = float('inf')  # set to infinity
    nearest_lat = None
    nearest_lon = None

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            file_lat = float(row[0])
            file_lon = float(row[1])

            dist = distance(float(given_lat), float(given_lon), file_lat, file_lon)

            if dist < nearest_dist:
                nearest_dist = dist
                nearest_lat = file_lat
                nearest_lon = file_lon

    return nearest_lat, nearest_lon


# convert from coordinates to indices
def convert_coord(lat, lon, csv_file):
    print(lat)
    print(lon)

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            # new nodes file as them switched
            if lat == float(row[0]) and lon == float(row[1]):
                return count
            else:
                count = count + 1


def draw_route_from_coordinates(start_coords, end_coords, edges_file='edges.csv', nodes_file='nodes.csv'):
    # Convert from coordinates to indices
    start_index = convert_coord(*nearest(nodes_file, *start_coords), nodes_file)
    end_index = convert_coord(*nearest(nodes_file, *end_coords), nodes_file)

    #print(start_index)
    #print(end_index)

    # Plot optimal route between two nodes
    map_obj = draw_optimal_route(nodes_file, start_index, end_index, predecessors)
    map_obj.save('my_map.html')
    webbrowser.open('my_map.html', new=2)


start_coords = [sys.argv[1], sys.argv[2]]
end_coords = [sys.argv[3], sys.argv[4]]

draw_route_from_coordinates(start_coords, end_coords)

# Plot all data points
# map_all = plot_all_data_on_map('nodes.csv')
# map_all.save('my_map_all.html')
# webbrowser.open('my_map_all.html', new=2)
