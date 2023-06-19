import csv
from math import asin, cos, sqrt, radians


# calculates distance between two sets of longitude and latitude
def distance(lat1, lon1, lat2, lon2):
    # approximate radius of Earth in km
    R = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # haversine formula to calculate distance
    hav = 0.5 - cos(lat2_rad-lat1_rad)/2 + cos(lat1_rad)*cos(lat2_rad) * (1-cos(lon2_rad-lon1_rad)) / 2
    return R * asin(sqrt(hav))

# uses distance function to find nearest pair of longitude and latitude in a given file to a given pair
def nearest(csv_file, given_lat, given_lon):
    nearest_dist = float('inf') # set to infinity
    nearest_lat = None
    nearest_lon = None

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            file_lat = float(row[0])
            file_lon = float(row[1])

            dist = distance(given_lat, given_lon, file_lat, file_lon)

            if dist < nearest_dist:
                nearest_dist = dist
                nearest_lat = file_lat
                nearest_lon = file_lon

    return nearest_lat, nearest_lon


# test
# given_lat = 38.995242
# given_lon = -76.937380
# csv_file = 'nodes.csv'
# nearest_lat, nearest_lon = nearest(csv_file, given_lat, given_lon)

# print(f"Lat: {nearest_lat}, Lon: {nearest_lon}")