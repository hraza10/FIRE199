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


# Plot all data points
map_all = plot_all_data_on_map('nodes.csv')
map_all.save('my_map_all.html')
webbrowser.open('my_map_all.html', new=2)

# Plot optimal route between two nodes
#map_obj = draw_optimal_route('nodes.csv', 20, 100, predecessors)
#map_obj.save('my_map.html')
#webbrowser.open('my_map.html', new=2)
