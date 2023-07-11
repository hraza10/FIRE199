# This program uses the customtkinter and tkintermapview libraries developed by Tom Schimansky
# Source: https://github.com/TomSchimansky/TkinterMapView

import customtkinter as ctk
from tkintermapview import TkinterMapView

ctk.set_default_color_theme("blue")

class App(ctk.CTk): 
    
    APP_NAME = "Routing Application"
    WIDTH = 600
    HEIGHT = 400 
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        
        # ============ basic attributes ============
        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        
        self.start_marker_list = [] 
        self.end_marker_list = []
        self.marker_list = [] 
        # ============ creates four CTkFrames ============
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 0)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        
        self.frame_left = ctk.CTkFrame(master = self, width = 150, 
                                                 corner_radius = 0, fg_color = None)
        self.frame_center = ctk.CTkFrame(master = self, width = 300, 
                                                  corner_radius = 0, fg_color = None)
        self.frame_right = ctk.CTkFrame(master = self, width = 150, 
                                                 corner_radius = 0, fg_color = None)
        self.frame_bottom = ctk.CTkFrame(master = self, width = 150, 
                                                  corner_radius = 0, fg_color = None)
       
        self.frame_left.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew")
        self.frame_center.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "nsew")
        self.frame_right.grid(row = 0, column = 2, padx = 0, pady = 0, sticky = "nsew")
        self.frame_bottom.grid(row = 1, column = 0, columnspan = 3, padx = 0, pady = 0,
                              sticky = "nsew")
        # ============ frame_left ============
        self.start_marker_button = ctk.CTkButton(master = self.frame_left, 
                                                        text = "Set Start Marker", 
                                                        command = self.set_marker_event)
       
        self.end_marker_button = ctk.CTkButton(master = self.frame_left, 
                                                        text = "Set End Marker",
                                                        command = self.end_marker_event)
        self.clear_marker_button = ctk.CTkButton(master = self.frame_left,
                                                        text = "Clear Markers", 
                                                        command = self.clear_marker_event)
        self.start_marker_button.grid(pady = (20, 0), padx = (20, 20), row = 0, column = 0)
        self.end_marker_button.grid(pady = (20, 0), padx = (20, 20), row = 1, column = 0)
        self.clear_marker_button.grid(pady = (20, 0), padx = (20, 20), row = 2, column = 0)

        # ============ frame_center ============
        self.longitude_label1 = ctk.CTkLabel(master = self.frame_center, 
                                                       text = "Starting Longitude", 
                                                       font = ("Arial", 14))
        self.longitude_value1 = ctk.CTkLabel(master = self.frame_center, 
                                                       text = "------------", 
                                                       font = ("Arial", 14))
        self.latitude_label1 = ctk.CTkLabel(master = self.frame_center, 
                                                      text = "Starting Latitude", 
                                                      font = ("Arial", 14))
        self.latitude_value1 = ctk.CTkLabel(master = self.frame_center,
                                                      text = "-------------", 
                                                      font = ("Arial", 14))
        self.longitude_label2 = ctk.CTkLabel(master = self.frame_center, 
                                                       text = "Ending Longitude", 
                                                       font = ("Arial", 14))
        self.longitude_value2 = ctk.CTkLabel(master = self.frame_center, 
                                                       text = "------------", 
                                                       font = ("Arial", 14))
        self.latitude_label2 = ctk.CTkLabel(master = self.frame_center, 
                                                      text = "Ending Latitude", 
                                                      font = ("Arial", 14))
        self.latitude_value2 = ctk.CTkLabel(master = self.frame_center,
                                                      text = "-------------", 
                                                      font = ("Arial", 14))
        
        self.longitude_label1.grid(row=0, column=0, padx=10, pady=10)
        self.longitude_value1.grid(row=1, column=0, padx=10, pady=10)
        self.latitude_label1.grid(row=0, column=1, padx=10, pady=10)
        self.latitude_value1.grid(row=1, column=1, padx=10, pady=10)
        self.longitude_label2.grid(row=2, column=0, padx=10, pady=10)
        self.longitude_value2.grid(row=3, column=0, padx=10, pady=10)
        self.latitude_label2.grid(row=2, column=1, padx=10, pady=10)
        self.latitude_value2.grid(row=3, column=1, padx=10, pady=10)
        # ============ frame_right ============
        self.map_label = ctk.CTkLabel(self.frame_right, text = "Tile Server:", anchor = "w")
        self.map_option_menu = ctk.CTkOptionMenu(self.frame_right, values = ["OpenStreetMap", "Google Normal", "Google Satellite"],
                                                command = self.change_map)
        self.calculate_button = ctk.CTkButton(master = self.frame_right, text = "Calculate",
                                             command = self.calculate_route)
        
        self.map_label.grid(row = 0, column = 0, padx = (20, 20), pady = (10, 0))
        self.map_option_menu.grid(row = 1, column = 0, padx = (20, 0), pady = (10, 0))
        self.calculate_button.grid(row = 2, column = 0, padx = (20, 0), pady = (10, 0))
        
        # ============ frame_bottom ============
        self.frame_bottom.grid_rowconfigure(0, weight = 0)
        self.frame_bottom.grid_rowconfigure(1, weight = 1)
        self.frame_bottom.grid_columnconfigure(0, weight = 1)
        self.frame_bottom.grid_columnconfigure(1, weight = 0)
        self.frame_bottom.grid_columnconfigure(2, weight = 1)
        
        self.map_widget = TkinterMapView(master = self.frame_bottom, corner_radius = 0)
        self.entry = ctk.CTkEntry(master = self.frame_bottom, 
                                           placeholder_text = "type address")
        self.entry.bind("<Return>", self.search_event)
        self.entry_button = ctk.CTkButton(master = self.frame_bottom, text = "Search", 
                                         width = 60, command = self.search_event)
        
        self.map_widget.grid(row = 1, rowspan = 1, columnspan = 3, sticky = "nswe", padx = (0, 0), pady = (0, 0))
        self.entry.grid(row = 0, column = 0, sticky = "we", padx=(12, 0), pady = (12, 0))
        self.entry_button.grid(row = 0, column = 1, sticky = "w", padx = (12, 0), pady = (12, 0))
        
        # sets default options
        self.map_widget.set_address("University of Maryland College Park")
        self.map_option_menu.set("OpenStreetMap")
        
    # ============ button functionality ============
    def search_event(self, event = None): 
        self.map_widget.set_address(self.entry.get())
        
    def set_marker_event(self): 
        for marker in self.start_marker_list:
            marker.delete()
            
        start_position = self.map_widget.get_position()
        self.start_marker_list.append(self.map_widget.set_marker(start_position[0], start_position[1]))
        
        self.longitude_value1.configure(text = str(start_position[0]))
        self.latitude_value1.configure(text = str(start_position[1]))
        
    def end_marker_event(self): 
        for marker in self.end_marker_list: 
            marker.delete()
            
        end_position = self.map_widget.get_position()
        self.end_marker_list.append(self.map_widget.set_marker(end_position[0], end_position[1]))
        
        self.longitude_value2.configure(text = str(end_position[0]))
        self.latitude_value2.configure(text = str(end_position[1]))
        
    def clear_marker_event(self):
        for marker in self.start_marker_list:
            marker.delete()
        for marker in self.end_marker_list: 
            marker.delete()
        for marker in self.marker_list:
            marker.delete()
        
        self.longitude_value1.configure(text = "------------")
        self.latitude_value1.configure(text = "------------")
        self.longitude_value2.configure(text = "------------")
        self.latitude_value2.configure(text = "------------")
        
    def calculate_route(self):
        print("Hello World")
        
    def change_map(self, new_map: str): 
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google Normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google Satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    
    def on_closing(self, event = 0): 
        self.destroy()
        
    def start(self): 
        self.mainloop()
        
if __name__ == "__main__":
    app = App()
    app.start() 
