import csv
import gpxpy
import os

folder_path = 'gpx_files'
csv_folder = 'csv_files' 

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
                   
# Gets a list of all files in gpx_files
gpx_list = os.listdir(folder_path)

# Iterates over each of the files.
for file_name in gpx_list:
    file_path = os.path.join(folder_path, file_name)
    if (os.path.isfile(file_path)): # Checks for file directories.
        # Converts each of the gpx files to csv files.
        gpx_name = os.path.splitext(os.path.basename(file_path))[0]
        csv_name = os.path.join(csv_folder, gpx_name + '.csv')
        gpx_to_csv(file_path, csv_name)

               
